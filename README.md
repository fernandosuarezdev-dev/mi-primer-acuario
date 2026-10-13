# Mi Primer Acuario

Simulador de acuario en tiempo real para aprender a cuidar peces con la práctica. Funciona como app para Android y iPhone (Capacitor) y como página web.

## Estructura

| Carpeta / archivo | Qué es |
| --- | --- |
| `src/app.html` | La app completa (HTML, CSS y JavaScript en un solo archivo). Es la fuente de todo. |
| `src/native.js` | Puente con el teléfono: guardado durable, avisos, vibración, botón atrás, compartir copia. |
| `scripts/build-web.mjs` | Arma `www/` para el teléfono: fuentes locales, metas móviles y el puente compilado. |
| `capacitor.config.json` | Nombre, identificador (`com.miprimeracuario.app`) y ajustes nativos. |
| `android/`, `ios/` | Proyectos nativos generados por Capacitor. |
| `design/` | Arte del ícono, splash y gráfico de la tienda, y los scripts que los generan. |
| `store/` | Recursos para la ficha de Google Play (ícono 512, gráfico destacado, capturas). |
| `PRIVACIDAD.md` | Política de privacidad pública. |

## Compilar

Cada `push` a `main` compila la app en GitHub Actions (`.github/workflows/android.yml`) y publica los archivos en **Releases**:

- `*-google-play.aab`: lo que se sube a Google Play Console.
- `*-instalable.apk`: firmado, para instalar directo o subir a otras tiendas.
- `*-prueba.apk`: versión de prueba.

La firma usa dos secretos del repositorio: `ANDROID_KEYSTORE_BASE64` y `ANDROID_KEYSTORE_PASSWORD`. Sin ellos solo se genera el APK de prueba. La llave **nunca** se guarda en el repositorio.

En un computador con Node 22, JDK 21 y Android Studio:

```bash
npm ci
npm run sync          # arma www/ y lo copia a android/ e ios/
npx cap open android  # abre el proyecto en Android Studio
```

Para iPhone hace falta un Mac con Xcode y una cuenta de Apple Developer: `npx cap open ios`.

## Cambiar el ícono

Edita `design/art.js` y ejecuta `npm run icons`.
