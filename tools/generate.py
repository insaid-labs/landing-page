from pathlib import Path
from jinja2 import Environment, BaseLoader
import json, shutil
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CONTENT = ROOT / "src/content"
DIST = ROOT / "dist"
PATHS = {
 "arrow": "M7 17 17 7M7 7h10v10", "right": "M5 12h14m-5-5 5 5-5 5", "down": "M12 5v14m-5-5 5 5 5-5",
 "chevron": "m8 10 4 4 4-4", "plus": "M12 5v14M5 12h14", "close": "m6 6 12 12M6 18 18 6",
 "code": "m8 8-4 4 4 4m8-8 4 4-4 4m-3-11-2 14",
 "shield": "M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6l-8-3Zm-4 9 3 3 5-6",
 "spark": "m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3ZM20 2v4m-2-2h4",
 "cloud": "M6 18a5 5 0 0 1-1-9.9 7 7 0 0 1 13.5 1.4A4.5 4.5 0 0 1 18 18M12 13v9m-3-3 3 3 3-3",
 "pin": "M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 0 1 14 0ZM12 7a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z",
 "check": "m5 12 4 4L19 6", "checkcircle": "M22 11v1a10 10 0 1 1-6-9m-7 8 3 3L22 4",
 "lock": "M6 10h12v11H6V10Zm3 0V6a3 3 0 0 1 6 0v4",
 "bolt": "m13 2-9 12h7l-1 8 10-13h-7l1-7Z",
 "chat": "M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9H13a8.5 8.5 0 0 1 8 8v.5Z",
 "layers": "m12 3 10 6-10 6L2 9l10-6Zm-10 12 10 6 10-6M2 12l10 6 10-6",
 "users": "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm13 18v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
 "target": "M21 12a9 9 0 1 1-9-9m0 4a5 5 0 1 0 5 5m-5 0 9-9m-4 0h4v4",
 "building": "M3 21h18M5 21V7h14v14M9 7V3h6v4M9 11h1m4 0h1m-6 4h1m4 0h1M10 21v-3h4v3",
 "heart": "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z",
 "linkedin": "M4 9v12m0-18v1m5 17V9h4v2a4 4 0 0 1 8 2v8m-8 0v-8",
 "github": "M9 19c-4 1-4-2-6-2m13 5v-4a3.5 3.5 0 0 0-1-2.8c3-.3 6-1.5 6-7A5.4 5.4 0 0 0 19.5 5 5 5 0 0 0 19.4 1S18.2.7 15 2.5a14 14 0 0 0-6 0C5.8.7 4.6 1 4.6 1A5 5 0 0 0 4.5 5 5.4 5.4 0 0 0 3 8.8c0 5.5 3 6.7 6 7A3.5 3.5 0 0 0 8 18v4",
 "menu": "M4 7h16M4 12h16M4 17h16",
 "globe": "M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM3 12h18M12 3a18 18 0 0 0 0 18 18 18 0 0 0 0-18Z",
 "pharma": "M10 3h4v7h7v4h-7v7h-4v-7H3v-4h7V3Z",
 "game": "M8 8h8c4 0 5 10 3 11-2 1-4-3-5-3h-4c-1 0-3 4-5 3-2-1-1-11 3-11Zm-1 3v4m-2-2h4m6-1h.01m2 2h.01M10 8V5h4",
 "terminal": "m5 7 5 5-5 5m8 0h6", "chart": "M3 3v18h18M7 14l4-4 4 2 6-7"
}
def icon(name):
    return f"<svg class=\"icon\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"{PATHS[name]}\"/></svg>"
MARK = """<svg class="brand-mark" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M5 5h16v16H5zM15 15h16v16H15z" stroke="currentColor" stroke-width="3.5"/><path d="M15 15h6v6h-6z" fill="currentColor"/></svg>"""
FOUNDERS = [
 {"name":"Gabriel González", "surname":"González", "initials":"GG", "github":"Nuggetnuclear", "linkedin":"gabrielgonzalezl", "index":"01"},
 {"name":"Ezequiel Morales", "surname":"Morales", "initials":"EM", "github":"Forcexdev", "linkedin":"ezequielleandromorales", "index":"02"},
 {"name":"Maximiliano Solorza", "surname":"Solorza", "initials":"MS", "github":"Maxxee1", "linkedin":"maximilianosolorza", "index":"03"}
]
env=Environment(loader=BaseLoader(), autoescape=False)
metadata={}
for lang in ["es", "en"]:
    def t(es,en): return es if lang == "es" else en
    home = "/" if lang == "es" else "/en"
    title = t("InsideLabs — Tu próximo salto. Lo construimos.", "InsideLabs — Your next big step. We build it.")
    description = t("Software a medida, IA y automatización, ciberseguridad y cloud. Un equipo de 3 socios en Chile que construye soluciones reales. Hablemos de tu proyecto.", "Custom software, AI and automation, cybersecurity, and cloud. A team of 3 co-founders in Chile building real solutions. Let’s talk about your project.")
    services = [
      ("code", t("Software a medida", "Custom software"), t("Sistemas, plataformas web e integraciones que se adaptan a tu operación.", "Systems, web platforms, and integrations that fit the way you work."), "React · Java · TypeScript"),
      ("spark", t("IA y automatización", "AI & automation"), t("Automatiza lo repetitivo. Chatbots por WhatsApp y atención 24/7.", "Automate repetitive work. WhatsApp chatbots and 24/7 support."), "Gemini · Embeddings · NLP"),
      ("shield", t("Ciberseguridad", "Cybersecurity"), t("Detecta riesgos antes de que sean problemas. Auditoría y desarrollo seguro.", "Find risks before they become problems. Auditing and secure development."), "Pentesting · Security-first"),
      ("cloud", t("Soluciones cloud", "Cloud solutions"), t("Infraestructura para crecer. Microservicios, despliegues y CI/CD.", "Infrastructure for growth. Microservices, deployments, and CI/CD."), "Google Cloud · CI/CD")
    ]
    benefits = [
      ("shield",t("Seguridad en el ADN", "Security in our DNA"),t("Nuestro origen en seguridad ofensiva nos enseñó a pensar en lo que puede fallar, antes de que falle.", "Our offensive security roots taught us to think about what could go wrong, before it does.")),
      ("users",t("Cerca de ti, dentro del proyecto", "Close to you, hands-on in the project"),t("Trabajas directamente con los 3 socios. Sin capas de gestión ni mensajes que se pierden en el camino.", "Work directly with the 3 co-founders. No layers of management or messages lost along the way.")),
      ("target",t("Tu negocio antes que el stack", "Your business before the stack"),t("Primero entendemos tu problema. Después elegimos la tecnología. Cada decisión tiene una razón.", "First, we understand your problem. Then we choose the technology. Every decision has a reason.")),
      ("layers",t("Construido para lo que sigue", "Built for what comes next"),t("Código mantenible, infraestructura escalable y decisiones técnicas pensadas más allá del lanzamiento.", "Maintainable code, scalable infrastructure, and technical decisions that go beyond launch day."))
    ]
    faqs = [
      (t("¿Cómo empezamos a trabajar juntos?", "How do we start working together?"), t("Escríbele a cualquiera de los socios por LinkedIn. Conversamos sobre tu desafío, revisamos el alcance y preparamos una propuesta con entregables, etapas y condiciones claras antes de empezar.", "Message any co-founder on LinkedIn. We’ll discuss your challenge, review the scope, and prepare a proposal with clear deliverables, milestones, and terms before we start.")),
      (t("¿Cuánto cuesta desarrollar un proyecto?", "How much does a project cost?"),t("Depende del alcance, las integraciones y la complejidad. No usamos una tarifa genérica para problemas distintos. Después de entender lo que necesitas, entregamos una cotización específica para tu proyecto.", "It depends on scope, integrations, and complexity. Different problems shouldn’t have a one-size-fits-all price. Once we understand your needs, we provide a project-specific quote.")),
      (t("¿Pueden automatizar el soporte de mi empresa?", "Can you automate support for my company?"),t("Sí. La plataforma creada para GameClub atiende por WhatsApp 24/7 y es replicable para otros clientes. Adaptamos los flujos, el conocimiento y las reglas de asignación a tu operación. Primero evaluamos qué conviene automatizar y dónde aporta la IA.", "Yes. The platform built for GameClub provides 24/7 WhatsApp support and can be replicated for other clients. We adapt the flows, knowledge, and assignment rules to your operation. First, we assess what to automate and where AI adds value.")),
      (t("¿Trabajan con sistemas que ya existen?", "Do you work with existing systems?"),t("Sí. Podemos evaluar tu plataforma actual, construir integraciones API y modernizar componentes. El primer paso es revisar la arquitectura, los accesos y las restricciones para proponer una evolución realista.", "Yes. We can assess your current platform, build API integrations, and modernize components. We start by reviewing the architecture, access, and constraints to propose a realistic way forward.")),
      (t("¿Qué pasa después del lanzamiento?", "What happens after launch?"),t("Acordamos contigo el alcance del acompañamiento, mantenimiento y evolución. Los tiempos de respuesta, responsabilidades y condiciones quedan definidos en la propuesta de tu proyecto.", "We agree on the scope of ongoing support, maintenance, and development with you. Response times, responsibilities, and terms are defined in your project proposal.")),
      (t("¿Solo trabajan con empresas de Chile?", "Do you only work with companies in Chile?"),t("Estamos en Chile y podemos conversar sobre proyectos remotos. Revisamos juntos los requisitos de idioma, coordinación, pagos y regulación antes de comprometernos con el alcance.", "We’re based in Chile and are open to discussing remote projects. We review language, coordination, payment, and regulatory requirements together before committing to a scope."))
    ]
    service_details = [
        {"items": [t("Plataformas web, PWA y sistemas de gestión.", "Web platforms, PWAs, and management systems."), t("Dashboards e integraciones con tus herramientas.", "Dashboards and integrations with your tools."), t("Modelos de datos y reglas propios de tu operación.", "Data models and rules tailored to your operation.")], "case": "case-pharma", "label": t("Ver un ejemplo: PharmaLogic", "See an example: PharmaLogic")},
        {"items": [t("Atención por WhatsApp y flujos automatizados 24/7.", "WhatsApp support and automated workflows 24/7."), t("Tickets con asignación automática y memoria de conversación.", "Automatically assigned tickets and conversation memory."), t("IA donde aporta; reglas claras donde no hace falta.", "AI where it helps; clear rules where it is not needed.")], "case": "case-gameclub", "label": t("Ver un ejemplo: GameClub", "See an example: GameClub")},
        {"items": [t("Revisión de riesgos y auditoría según alcance acordado.", "Risk reviews and auditing within an agreed scope."), t("Desarrollo con seguridad desde el diseño.", "Security-by-design software development."), t("Hallazgos y prioridades para fortalecer tu aplicación.", "Findings and priorities to strengthen your application.")], "case": None, "label": ""},
        {"items": [t("Despliegues en Google Cloud Run y contenedores.", "Deployments on Google Cloud Run and containers."), t("Microservicios e integración y entrega continuas.", "Microservices and continuous integration and delivery."), t("Infraestructura alineada con las necesidades del proyecto.", "Infrastructure aligned with your project’s needs.")], "case": "case-gameclub", "label": t("Ver arquitectura aplicada: GameClub", "See the architecture in action: GameClub")},
    ]
    portrait_urls = {
        "Nuggetnuclear": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=800&h=1000&q=85",
        "Forcexdev": "https://images.unsplash.com/photo-1594672830234-ba4cfe1202dc?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Maxxee1": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=800&h=1000&q=85",
    }
    stack_logos = [
        {"name":"React", "slug":"react", "url":"https://react.dev/"},
        {"name":"Next.js", "slug":"nextjs", "url":"https://nextjs.org/"},
        {"name":"TypeScript", "slug":"typescript", "url":"https://www.typescriptlang.org/"},
        {"name":"Node.js", "slug":"nodejs", "url":"https://nodejs.org/"},
        {"name":"Spring Boot", "slug":"spring", "url":"https://spring.io/projects/spring-boot"},
        {"name":"Google Cloud", "slug":"googlecloud", "url":"https://cloud.google.com/"},
    ]
    for tech in stack_logos:
        if tech["slug"] in ("nextjs", "typescript", "nodejs"):
            tech["asset"] = "https://cdn.jsdelivr.net/gh/devicons/devicon@master/icons/" + tech["slug"] + "/" + tech["slug"] + "-original.svg"
        else:
            tech["asset"] = "/images/stack/" + tech["slug"] + ".svg"
    testimonials = [
        {"text": t("“Que las consultas repetitivas se resuelvan por WhatsApp, incluso de noche, nos deja tiempo para los casos que necesitan una persona.”", "“When repetitive questions are handled on WhatsApp, even at night, we have more time for the cases that need a person.”"), "role": t("Responsable de soporte", "Support lead"), "context": t("Escenario ilustrativo · GameClub", "Illustrative scenario · GameClub"), "icon": "chat"},
        {"text": t("“Ver los lotes, sus vencimientos y el inventario en un mismo lugar cambia la forma en que organizamos los despachos.”", "“Seeing batches, expiry dates, and inventory in one place changes how we organize dispatches.”"), "role": t("Responsable de farmacia", "Pharmacy manager"), "context": t("Escenario ilustrativo · PharmaLogic", "Illustrative scenario · PharmaLogic"), "icon": "pharma"},
        {"text": t("“Lo importante no es solo saber cuánto vendí. Es entender qué combo deja ganancias después de los costos y las comisiones.”", "“It is not just about knowing what I sold. It is about knowing which combo is profitable after costs and fees.”"), "role": t("Dueño de negocio", "Business owner"), "context": t("Escenario ilustrativo · POS", "Illustrative scenario · POS"), "icon": "chart"},
    ]
    schema=json.dumps({"@context":"https://schema.org","@type":"Organization","name":"InsideLabs","url":"https://insidelabs.cl","description":description,"address":{"@type":"PostalAddress","addressCountry":"CL"},"founder":[{"@type":"Person","name":f["name"],"sameAs":["https://github.com/"+f["github"],"https://www.linkedin.com/in/"+f["linkedin"]+"/"]} for f in FOUNDERS]},ensure_ascii=False)
    ctx=dict(t=t,lang=lang,home=home,title=title,description=description,icon=icon,mark=MARK,services=services,benefits=benefits,faqs=faqs,founders=FOUNDERS,schema=schema,service_details=service_details,portrait_urls=portrait_urls,testimonials=testimonials,stack_logos=stack_logos)
    ctx["hero_photo"] = env.from_string((ROOT/"tools/hero-photo.html.j2").read_text()).render(**ctx)
    body=env.from_string((ROOT/"tools/brands.html.j2").read_text() + (ROOT/"tools/page.html.j2").read_text() + (ROOT/"tools/dialogs.html.j2").read_text()).render(**ctx)
    header=env.from_string((ROOT/"tools/header.html.j2").read_text()).render(**ctx)
    head=env.from_string((ROOT/"tools/head.html.j2").read_text()).render(**ctx)
    (CONTENT/f"{lang}.html").write_text(body)
    (CONTENT/f"{lang}-head.html").write_text(head)
    page=f"<!doctype html>\n<html lang=\"{lang}\"><head>{head}</head><body>{header}{body}</body></html>"
    out=DIST / ("en" if lang == "en" else "")
    out.mkdir(parents=True,exist_ok=True)
    (out/"index.html").write_text(page)
    metadata[lang]={"home":home,"title":title,"description":description,"skip":t("Saltar al contenido","Skip to content"),"navLabel":t("Navegación principal","Main navigation"),"mobileLabel":t("Navegación móvil","Mobile navigation"),"services":t("Servicios","Services"),"projects":t("Proyectos","Projects"),"about":t("Nosotros","About us"),"language":t("Seleccionar idioma","Choose language"),"talk":t("Hablemos","Let’s talk"),"talkLong":t("Hablemos de tu proyecto","Let’s talk about your project"),"open":t("Abrir menú","Open menu"),"homeLabel":t("inicio","home")}
(CONTENT/"locales.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
for item in PUBLIC.iterdir():
    if item.is_dir(): shutil.copytree(item,DIST/item.name,dirs_exist_ok=True)
    else: shutil.copy2(item,DIST/item.name)
print("Generated Spanish and English routes, shared Astro content, and static preview.")

shutil.copy2(ROOT / "tools/404.html", DIST / "404.html")
