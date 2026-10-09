# InsideLabs — Landing Page

Landing page oficial de **InsideLabs** construida con Astro, React y TypeScript.

---

## Tecnologías

- **[Astro](https://astro.build/)** (v5 / v7) — Framework web optimizado para rendimiento y sitios estáticos.
- **[React](https://react.dev/)** — Componentes de interfaz de usuario.
- **[TypeScript](https://www.typescriptlang.org/)** — Tipado estático.

---

## Requisitos previos

- **Node.js** v20 o superior
- **npm** (o pnpm / yarn)

---

## Instalación y Desarrollo

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/insaid-labs/landing-page.git
   cd landing-page
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Iniciar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:3000`.

---

## Scripts disponibles

| Comando | Descripción |
| --- | --- |
| `npm run dev` | Inicia el entorno local de desarrollo con hot reload. |
| `npm run build` | Valida tipos (`astro check`) y compila el sitio para producción en `/dist`. |
| `npm run preview` | Previsualiza localmente el build de producción. |

---

## Estructura del Proyecto

```text
├── public/          # Recursos estáticos (estilos, imágenes, scripts de interacción)
├── src/
│   ├── components/  # Componentes React (Header, etc.)
│   ├── content/     # Contenido estático y traducciones (ES / EN)
│   ├── layouts/     # Layouts principales de Astro
│   └── pages/       # Rutas del sitio (/, /en, 404)
├── tools/           # Utilidades y scripts de soporte
└── astro.config.mjs # Configuración de Astro
```

---

## Despliegue

El proyecto está configurado para exportación estática (`output: 'static'`) y es compatible con plataformas como **Vercel**, **Netlify** o **GitHub Pages**. En Vercel se despliega automáticamente utilizando la configuración en `vercel.json` y la carpeta de salida `dist`.
