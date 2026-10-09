# InsideLabs — V9, regreso a fotografía

Se retira la animación del hero y su botón replay. El resto del contenido es idéntico al de V8: se verificó por comparación del DOM fuera de esa figura.

## Fotografía elegida

Portátil real, como referencia visual de software y tecnología. Sin placa de circuitos, collage, dispositivos inventados ni animación. Se conserva el caption “Construir bien. Pensar más allá.” y se aplica únicamente un ajuste ligero de color/contraste y una sombra inferior para el texto.

URL directa, no endpoint de descarga:
https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1600&q=90

**Límite importante:** la petición HTTPS desde este entorno falló por certificado TLS. No se pudo descargar, inspeccionar visualmente ni verificar el renderizado de la fotografía aquí. La URL directa está documentada en referencias públicas como una imagen de portátil; esto no equivale a una validación visual. Verificar en navegador antes de publicar. Si falla, aparece un mensaje explícito y enlace a la fotografía, no una animación sustitutiva.

El hero requiere Internet. También los retratos de referencia, tres iconos Devicon, favicon GameClub y fuentes web. Los recursos locales, CSS y JavaScript están incrustados en la vista previa.

## Abrir

Abrir `preview/InsideLabs-v9.html`. Idioma con `?lang=es` o `?lang=en`.

## Astro / Vercel

Astro + React renderizado solo en build + TypeScript. Español `/`, inglés `/en`, output estático sin hidratación React.

Con Node.js 22 o superior:

```sh
npm install
npm run dev
npm run build
npm run preview
```

Vercel usa `vercel.json` y salida `dist`. Sin secretos obligatorios.

Preview sin npm:

```sh
python tools/serve.py --port 3000
```

Si está ocupado, `--port 0` asigna un puerto libre.

## Edición y comprobación

- `tools/hero-photo.html.j2`: fotografía y caption.
- `tools/head.html.j2`: preload con la misma URL.
- `public/styles.css`: bloque V9.
- `public/interaction.js`: manejo de error/carga de imagen; se retiró replay.
- `tools/generate.py`: generación de contenido.

```sh
python tools/generate.py
node --check public/interaction.js
node tools/verify-interactions.cjs
python tools/verify-site.py
```

Tests estructurales y de lógica con DOM simulado: foto directa, ausencia de animación, preservación del resto de la página, contacto, filtros, modales, foco y fallbacks. No hay navegador ni npm disponibles aquí; build Astro, inspección visual, assets remotos y auditoría accesible pendientes en el entorno de despliegue.

Se mantienen las condiciones previas: fotos de equipo y testimonios de referencia identificados, email placeholder, marcas provisionales documentadas y referencias legales sin certificación ni garantía de cumplimiento.
