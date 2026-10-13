// Puente entre la app web y el teléfono (Android / iPhone) usando Capacitor.
// Se compila con esbuild a www/native.js y deja disponible window.AQN.
// En el navegador (sin Capacitor) window.AQN queda en null y la app usa sus alternativas web.
import { Capacitor, SystemBars, SystemBarsStyle } from '@capacitor/core';
import { App } from '@capacitor/app';
import { Haptics, ImpactStyle, NotificationType } from '@capacitor/haptics';
import { LocalNotifications } from '@capacitor/local-notifications';
import { Preferences } from '@capacitor/preferences';
import { SplashScreen } from '@capacitor/splash-screen';
import { Filesystem, Directory, Encoding } from '@capacitor/filesystem';
import { Share } from '@capacitor/share';

const CHANNEL = 'cuidados';
const DAILY_ID = 900;

function makeBridge() {
  const platform = Capacitor.getPlatform();
  let channelReady = null;
  const ensureChannel = () => {
    if (platform !== 'android') return Promise.resolve();
    if (!channelReady) {
      channelReady = LocalNotifications.createChannel({
        id: CHANNEL,
        name: 'Cuidados del acuario',
        description: 'Avisos cuando tus peces necesitan algo',
        importance: 4,
        visibility: 1,
        vibration: true,
        lights: true,
        lightColor: '#40E0E8',
      }).catch(() => {});
    }
    return channelReady;
  };

  try { SystemBars.setStyle({ style: SystemBarsStyle.Dark }); } catch (e) { /* opcional */ }

  return {
    platform,
    async version() {
      const i = await App.getInfo();
      return i.version;
    },
    store: {
      async get(key) { return (await Preferences.get({ key })).value; },
      set(key, value) { return Preferences.set({ key, value }); },
      remove(key) { return Preferences.remove({ key }); },
    },
    haptic(n) {
      try {
        if (Array.isArray(n)) Haptics.notification({ type: NotificationType.Success });
        else Haptics.impact({ style: n >= 12 ? ImpactStyle.Medium : ImpactStyle.Light });
      } catch (e) { /* sin vibración */ }
    },
    notif: {
      async status() { return (await LocalNotifications.checkPermissions()).display; },
      async request() {
        await ensureChannel();
        return (await LocalNotifications.requestPermissions()).display;
      },
      // Reemplaza todos los avisos pendientes por la lista dada (+ recordatorio diario si hour >= 0).
      async replace(list, hour) {
        const perm = (await LocalNotifications.checkPermissions()).display;
        const pending = (await LocalNotifications.getPending()).notifications || [];
        if (pending.length) await LocalNotifications.cancel({ notifications: pending.map((n) => ({ id: n.id })) });
        if (perm !== 'granted') return;
        await ensureChannel();
        const notifications = list.map((n) => ({
          id: n.id,
          title: n.title,
          body: n.body,
          largeBody: n.body,
          schedule: { at: new Date(n.at), allowWhileIdle: true },
          channelId: CHANNEL,
          extra: { tank: n.tank },
        }));
        if (hour != null && hour >= 0) {
          notifications.push({
            id: DAILY_ID,
            title: 'Tu acuario te espera',
            body: 'Pasa a ver cómo están tus peces y haz las labores del día.',
            schedule: { on: { hour, minute: 0 }, allowWhileIdle: true },
            channelId: CHANNEL,
            extra: {},
          });
        }
        if (notifications.length) await LocalNotifications.schedule({ notifications });
      },
      onTap(fn) {
        LocalNotifications.addListener('localNotificationActionPerformed', (e) => {
          try { fn((e && e.notification && e.notification.extra) || {}); } catch (err) { console.error(err); }
        });
      },
    },
    async shareFile(name, text) {
      const r = await Filesystem.writeFile({ path: name, data: text, directory: Directory.Cache, encoding: Encoding.UTF8 });
      await Share.share({ title: 'Copia de Mi Primer Acuario', text: 'Copia de seguridad de Mi Primer Acuario', files: [r.uri], dialogTitle: 'Guardar o enviar la copia' });
    },
    onBack(fn) { App.addListener('backButton', () => fn()); },
    onState(fn) { App.addListener('appStateChange', (s) => fn(!!s.isActive)); },
    minimize() { return App.minimizeApp().catch(() => App.exitApp()); },
    hideSplash() { return SplashScreen.hide({ fadeOutDuration: 300 }).catch(() => {}); },
  };
}

window.AQN = Capacitor.isNativePlatform() ? makeBridge() : null;
