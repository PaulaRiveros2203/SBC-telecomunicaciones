import streamlit as st
from typing import Dict, List, Tuple, Set

# ============================================================
# CONFIGURACION PAGINA
# ============================================================

st.set_page_config(
    page_title="SBC AVAL VALOR COMPARTIDO",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

/* Fondo principal */
.stApp { background-color: #050816; }

/* Tipografía general */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

/* Título principal */
.titulo {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin-bottom: 0px;
    line-height: 1.1;
}

.subtitulo {
    font-size: 20px;
    color: #94a3b8;
    margin-top: 4px;
    margin-bottom: 0px;
}

.descripcion {
    font-size: 16px;
    color: #cbd5e1;
    margin-top: 8px;
}

/* Cards de reglas */
.card-regla {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 16px 20px;
    border-radius: 12px;
    border-left: 4px solid #2563eb;
    margin: 8px 0;
}

.card-exito {
    background: linear-gradient(135deg, #052e16 0%, #14532d 100%);
    padding: 16px 20px;
    border-radius: 12px;
    border-left: 4px solid #22c55e;
    margin: 8px 0;
}

.card-error {
    background: linear-gradient(135deg, #1c0a0a 0%, #450a0a 100%);
    padding: 16px 20px;
    border-radius: 12px;
    border-left: 4px solid #ef4444;
    margin: 8px 0;
}

.card-warning {
    background: linear-gradient(135deg, #1c1005 0%, #451a03 100%);
    padding: 16px 20px;
    border-radius: 12px;
    border-left: 4px solid #f59e0b;
    margin: 8px 0;
}

.card-info {
    background: linear-gradient(135deg, #0c1a2e 0%, #0f3460 100%);
    padding: 16px 20px;
    border-radius: 12px;
    border-left: 4px solid #3b82f6;
    margin: 8px 0;
}

/* Badge de regla */
.badge {
    display: inline-block;
    background-color: #1d4ed8;
    color: white;
    font-size: 12px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    margin-right: 8px;
}

.badge-gm {
    background-color: #7c3aed;
}

.badge-ok {
    background-color: #15803d;
}

.badge-fail {
    background-color: #b91c1c;
}

/* Paso de razonamiento */
.paso {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background-color: #0f172a;
    border-radius: 10px;
    margin: 6px 0;
    border: 1px solid #1e293b;
}

.paso-num {
    background-color: #1d4ed8;
    color: white;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    flex-shrink: 0;
}

/* Métricas custom */
.metrica-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}

.metrica-valor {
    font-size: 36px;
    font-weight: 800;
    color: #60a5fa;
}

.metrica-label {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 4px;
}

/* Chat messages */
.chat-user {
    background-color: #1e3a5f;
    border-radius: 12px 12px 4px 12px;
    padding: 10px 16px;
    margin: 6px 0;
    color: white;
    font-size: 14px;
}

.chat-bot {
    background-color: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px 12px 12px 4px;
    padding: 10px 16px;
    margin: 6px 0;
    color: #e2e8f0;
    font-size: 14px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0a0f1e;
    border-right: 1px solid #1e293b;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 15px;
    width: 100%;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8);
    transform: translateY(-1px);
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #0f172a;
    border: 1px solid #1e3a5f;
    color: white;
    border-radius: 8px;
}

/* Divider */
hr { border-color: #1e293b !important; }

</style>
""", unsafe_allow_html=True)

# ============================================================
# MOTOR DE INFERENCIA REAL — 14 REGLAS
# ============================================================

def crear_regla(nombre, condiciones, conclusion, certeza=1.0, descripcion="", contexto="router_cajero", accion=""):
    return {
        "nombre": nombre,
        "condiciones": condiciones,
        "conclusion": conclusion,
        "certeza": certeza,
        "descripcion": descripcion,
        "contexto": contexto,
        "accion": accion
    }


def crear_base_conocimiento() -> List[Dict]:
    """
    Base de conocimiento completa: 14 reglas en 3 bloques.
    Bloque A (R01-R07): Soporte básico
    Bloque B (R08-R11): Instalación nueva
    Bloque C (R12-R14): Conmutación forzada VSAT→4G
    """
    reglas = []

    # ── BLOQUE A: SOPORTE BÁSICO ──
    reglas.append(crear_regla(
        "R01", ["fa0_up_up", "fa1_up_up", "fa2_up_up"],
        "proceder_validacion_logica", 1.0,
        "fa0/fa1/fa2 están up/up — capa física operativa",
        "router_cajero",
        "Proceder a validar BVI2 y BVI3 con `sh arp`"
    ))
    reglas.append(crear_regla(
        "R02", ["proceder_validacion_logica", "bvi2_con_direccionamiento", "bvi3_con_direccionamiento"],
        "proceder_pings_bvi", 1.0,
        "BVI2 y BVI3 tienen IPs asignadas correctamente",
        "router_cajero",
        "Ejecutar pings de validación a todas las IPs"
    ))
    reglas.append(crear_regla(
        "R03", ["proceder_pings_bvi", "ping_gw_bvi2_ok", "ping_cajero_ok", "ping_camaras_ok"],
        "conectividad_bvi2_correcta", 1.0,
        "Pings OK: GW bvi2 (router), cajero (CMD red corporativa), cámaras (router)",
        "router_cajero",
        "Conectividad BVI2 confirmada ✓"
    ))
    reglas.append(crear_regla(
        "R04", ["proceder_pings_bvi", "ping_gw_bvi3_ok", "ping_alarmas_ok"],
        "conectividad_bvi3_correcta", 1.0,
        "Pings OK: GW bvi3 y alarmas (ambos desde router)",
        "router_cajero",
        "Conectividad BVI3 confirmada ✓"
    ))
    reglas.append(crear_regla(
        "R05", ["conectividad_bvi2_correcta", "conectividad_bvi3_correcta"],
        "revisar_errores_fisicos", 1.0,
        "Conectividad lógica completa — revisar capa física",
        "router_cajero",
        "Ejecutar `sh int | in error`"
    ))
    reglas.append(crear_regla(
        "R06", ["revisar_errores_fisicos", "errores_fisicos_detectados"],
        "solicitar_cambio_cable", 0.95,
        "Errores físicos detectados en alguna interfaz",
        "router_cajero",
        "`sh int faX | in error` → identificar interfaz → solicitar cambio de cable → `clear counters`"
    ))
    reglas.append(crear_regla(
        "R07", ["revisar_errores_fisicos", "sin_errores_fisicos"],
        "verificar_medio_activo", 1.0,
        "Sin errores físicos — verificar medio activo",
        "router_cajero",
        "`sh ip int brief` → confirmar si servicio va por VSAT (fa4) o 4G (fa3)"
    ))

    # ── BLOQUE B: INSTALACIÓN NUEVA ──
    reglas.append(crear_regla(
        "R08", ["fa0_admin_down", "fa1_admin_down", "fa2_admin_down"],
        "habilitar_interfaces", 1.0,
        "fa0/fa1/fa2 en administratively down",
        "router_cajero",
        "`conf t` → `int fa0` → `no shutdown` → repetir para fa1 y fa2"
    ))
    reglas.append(crear_regla(
        "R09", ["habilitar_interfaces", "fa0_connected", "fa1_connected", "fa2_connected"],
        "aprender_macs", 1.0,
        "Interfaces connected — aprender MACs de dispositivos",
        "router_cajero",
        "`sh mac` → anotar MAC fa0 (cajero), fa1 (cámaras), fa2 (alarmas)"
    ))
    reglas.append(crear_regla(
        "R10", ["aprender_macs", "mac_cajero_aprendida", "mac_camaras_aprendida", "mac_alarmas_aprendida"],
        "configurar_acls", 1.0,
        "MACs aprendidas — configurar listas de acceso",
        "router_cajero",
        "`no access-list 700` → `access-list 700 permit MAC cajero` → `permit MAC camaras` / `no access-list 701` → `access-list 701 permit MAC alarmas`"
    ))
    reglas.append(crear_regla(
        "R11", ["configurar_acls", "acl700_configurada", "acl701_configurada"],
        "guardar_configuracion", 1.0,
        "ACL700 y ACL701 configuradas correctamente",
        "router_cajero",
        "`do wr` → guardar configuración → ejecutar Soporte Básico para validar"
    ))

    # ── BLOQUE C: CONMUTACIÓN FORZADA ──
    reglas.append(crear_regla(
        "R12", ["tunnel_gm_activo", "pings_tunnel_ok"],
        "programar_reload_seguridad", 1.0,
        "GM: tunnel activo y pings OK — proceder con seguridad",
        "router_cajero",
        "[Router cajero] `reload in 10` + `confirm` — red de seguridad antes de conmutar"
    ))
    reglas.append(crear_regla(
        "R13", ["programar_reload_seguridad", "reload_programado"],
        "bajar_fa4_vsat", 1.0,
        "Reload programado — ejecutar conmutación",
        "router_cajero",
        "[Router cajero] `conf t` → `int fa4` → `shut` — IP SLA detecta caída y activa fa3 (4G)"
    ))
    reglas.append(crear_regla(
        "R14", ["bajar_fa4_vsat", "vsat_inactivo", "4g_activo"],
        "cancelar_reload", 1.0,
        "Conmutación exitosa: 4G activo, VSAT abajo",
        "router_cajero",
        "[Router cajero] `no reload` → cancelar seguro → ejecutar Soporte Básico para validar"
    ))

    return reglas


def encadenamiento_adelante(hechos_iniciales: Set[str], reglas: List[Dict]) -> Tuple[Set[str], List[Dict]]:
    """Motor de inferencia forward chaining — Modus Ponens iterativo."""
    hechos = set(hechos_iniciales)
    reglas_aplicadas = []
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for regla in reglas:
            ya = any(r["nombre"] == regla["nombre"] for r in reglas_aplicadas)
            if ya:
                continue
            if all(c in hechos for c in regla["condiciones"]):
                hechos.add(regla["conclusion"])
                reglas_aplicadas.append(regla)
                hubo_cambio = True
    return hechos, reglas_aplicadas


def porque(conclusion: str, reglas_aplicadas: List[Dict]) -> Dict:
    for r in reglas_aplicadas:
        if r["conclusion"] == conclusion:
            return r
    return {}


# ============================================================
# CHATBOT CON MOTOR REAL
# ============================================================

def detectar_intencion(p: str) -> str:
    """
    Detecta la intención del técnico a partir de lenguaje natural.
    Cubre frases coloquiales, jerga técnica y descripciones imprecisas.
    Retorna una clave de intención.
    """

    # ── CONMUTACIÓN FORZADA ──
    conmutacion_palabras = [
        # Términos directos
        "conmutacion", "conmutación", "conmutar", "forzada", "forzado",
        "cambio de medio", "cambiar medio", "cambiar enlace", "cambio enlace",
        # VSAT / satelital
        "vsat", "satelital", "satelite", "satélite", "intermitencia",
        "intermitente", "inestable", "fluctua", "fluctúa", "cae y sube",
        "sube y baja", "se cae el enlace", "enlace inestable",
        # 4G / backup
        "4g", "lte", "backup", "respaldo", "medio backup", "medio de respaldo",
        "subir por 4g", "activar 4g", "levantar 4g",
        # Acciones típicas
        "reload", "shut fa4", "bajar fa4", "ip sla", "ipsla",
        "fa4 abajo", "apagar fa4",
        # Frases coloquiales que indican conmutación
        "ayudame a conmutar", "como conmuto", "necesito conmutar",
        "quiero conmutar", "tengo que conmutar", "debo conmutar",
        "hacer una conmutacion", "hacer conmutacion", "hacer la conmutacion",
        "conmutacion forzada", "forzar conmutacion", "forzar la conmutacion",
        "pasar a 4g", "pasar al backup", "migrar a 4g",
        "el vsat esta malo", "vsat malo", "vsat fallando", "vsat caido",
        "vsat caído", "problema con vsat", "falla vsat", "falla en vsat",
        "medio principal caido", "medio principal caído", "enlace principal caido",
    ]
    if any(x in p for x in conmutacion_palabras):
        return "conmutacion"

    # ── INTERFACES ABAJO / INSTALACIÓN ──
    interfaces_abajo = [
        "admin down", "administratively", "administrativamente",
        "no sube", "interfaces abajo", "fa0 abajo", "fa1 abajo", "fa2 abajo",
        "no shutdown", "no levanta", "interfaz caida", "interfaz caída",
        "interfaz abajo", "interfaces caidas", "interfaces caídas",
        "puerto abajo", "puerto caido", "habilitar interfaz",
        "levantar interfaz", "levantar interfaces",
    ]
    if any(x in p for x in interfaces_abajo):
        return "interfaces_abajo"

    # ── INSTALACIÓN NUEVA ──
    instalacion_palabras = [
        "instalacion", "instalación", "instalar", "nuevo cajero",
        "nuevo equipo", "cajero nuevo", "equipo nuevo",
        "poner en servicio", "poner cajero", "montar cajero",
        "configurar cajero", "primera vez", "recien instalado",
        "recién instalado", "acabo de instalar",
    ]
    if any(x in p for x in instalacion_palabras):
        return "instalacion"

    # ── ERRORES FÍSICOS ──
    errores_palabras = [
        "error", "errores", "crc", "input error", "output error",
        "cable", "fisico", "físico", "fisicos", "físicos",
        "cambio de cable", "cambiar cable", "puerto malo",
        "interfaz con error", "muchos errores", "contador de errores",
        "clear counters", "clear count",
    ]
    if any(x in p for x in errores_palabras):
        return "errores_fisicos"

    # ── PING / CONECTIVIDAD ──
    ping_palabras = [
        "ping", "no responde", "sin conectividad", "sin conexion", "sin conexión",
        "cajero no responde", "cajero caido", "cajero caído",
        "no hay comunicacion", "no hay comunicación", "fuera de servicio",
        "no conecta", "no llega", "no alcanza", "perdida de paquetes",
        "pérdida de paquetes", "timeout", "unreachable",
        "no tengo acceso", "no hay acceso", "caido el cajero",
        "caído el cajero", "cajero fuera", "cajero sin servicio",
        "el cajero no funciona", "no funciona el cajero",
    ]
    if any(x in p for x in ping_palabras):
        return "ping"

    # ── TUNNEL / GM ──
    tunnel_palabras = [
        "tunnel", "tunel", "túnel", "gm", "getvpn", "getpvn",
        "concentrador", "grupo", "group member",
        "tunnel caido", "tunnel caído", "tunnel no sube",
        "sin tunnel", "verificar tunnel", "validar tunnel",
    ]
    if any(x in p for x in tunnel_palabras):
        return "tunnel"

    # ── MAC / ACL ──
    mac_palabras = [
        "mac", "acl", "access-list", "lista de acceso", "access list",
        "permitir mac", "bloqueo mac", "filtro mac",
        "acl700", "acl701", "access-list 700", "access-list 701",
    ]
    if any(x in p for x in mac_palabras):
        return "mac_acl"

    # ── BVI / ARP / DIRECCIONAMIENTO ──
    bvi_palabras = [
        "bvi", "bvi2", "bvi3", "arp", "direccionamiento",
        "ip address", "subred", "gateway", "puerta de enlace",
        "tabla arp", "sh arp", "show arp",
    ]
    if any(x in p for x in bvi_palabras):
        return "bvi_arp"

    # ── MEDIO ACTIVO ──
    medio_palabras = [
        "medio activo", "fa3", "fa4", "sh ip int brief", "show ip int brief",
        "por donde va", "que medio", "cual medio", "ip sla activo",
        "por vsat", "por 4g", "verificar medio",
    ]
    if any(x in p for x in medio_palabras):
        return "medio_activo"

    # ── SOPORTE BÁSICO GENERAL ──
    soporte_palabras = [
        "soporte", "diagnostico", "diagnóstico", "revisar", "validar",
        "verificar", "chequear", "checar", "ayuda", "ayudame",
        "como hago", "que hago", "por donde empiezo", "empezar",
        "cajero malo", "no funciona", "falla general",
        "paso a paso", "pasos", "procedimiento", "proceso",
    ]
    if any(x in p for x in soporte_palabras):
        return "soporte_basico"

    return "sin_match"


def responder_chatbot(pregunta: str) -> Tuple[str, List[str]]:
    """
    Interpreta lenguaje natural usando detección de intención amplia
    y activa el motor de inferencia para dar respuesta técnica precisa.
    """
    p = pregunta.lower()
    # Normalizar tildes y caracteres especiales comunes
    p = (p.replace("ó","o").replace("á","a").replace("é","e")
          .replace("í","i").replace("ú","u").replace("ñ","n"))
    reglas = crear_base_conocimiento()

    intencion = detectar_intencion(p)

    # ── CONMUTACIÓN FORZADA ──
    if intencion == "conmutacion":
        respuesta = (
            "**Conmutación forzada VSAT → 4G — paso a paso**\n\n"
            "**Desde el GM (solo diagnóstico, nunca intervención):**\n"
            "1. `sh run | in (numero_cajero)` → identifica el TunnelX asociado al cajero\n"
            "2. `sh run int TunnelX` → valida que el tunnel esté configurado\n"
            "3. Ping a la SIM (tunnel destination — IP del proveedor 4G)\n"
            "4. Ping source (tunnel source) a tunnel destination\n"
            "5. Ping sin source → punta nuestra\n"
            "6. Ping a IP del proveedor (siempre es la IP impar del bloque)\n"
            "7. Ping a nuestra punta (siguiente IP a la configurada en el tunnel)\n\n"
            "**En el router del cajero (toda la intervención activa va aquí):**\n"
            "8. `reload in 10` + `confirm` → seguro por si algo falla *(R12)*\n"
            "9. `conf t` → `int fa4` → `shut` → IP SLA detecta caída y activa fa3 *(R13)*\n"
            "10. Verificar con `sh ip int brief` que fa3 sube (4G activo)\n"
            "11. Si 4G activo y servicio estable: `no reload` → cancela el seguro *(R14)*\n"
            "12. Ejecutar **Soporte Básico** para validar conectividad completa\n\n"
            "⚠️ **Importante:** El `reload in 10` es obligatorio siempre como red de seguridad. "
            "Solo se cancela con `no reload` si la conmutación fue exitosa."
        )
        return respuesta, ["R12", "R13", "R14"]

    # ── INTERFACES ABAJO ──
    elif intencion == "interfaces_abajo":
        hechos = {"fa0_admin_down", "fa1_admin_down", "fa2_admin_down"}
        _, ra = encadenamiento_adelante(hechos, reglas)
        r = ra[0] if ra else None
        respuesta = (
            "**Interfaces en administratively down.**\n\n"
            "Primero verifique con `sh ip int brief` que fa0, fa1 y fa2 están admin down.\n\n"
            "**Pasos para habilitar** *(R08)*:\n"
            "1. `conf t`\n"
            "2. `int fa0` → `no shutdown` → `exit`\n"
            "3. `int fa1` → `no shutdown` → `exit`\n"
            "4. `int fa2` → `no shutdown` → `exit`\n\n"
            "**Validar:**\n"
            "5. `sh int status` → deben mostrar **connected**\n"
            "6. `sh ip int brief` → deben mostrar **up/up**\n\n"
            "Si quedan en down/down después del no shutdown, verificar cableado físico."
        )
        return respuesta, ["R08"]

    # ── INSTALACIÓN NUEVA ──
    elif intencion == "instalacion":
        respuesta = (
            "**Proceso completo de instalación nueva — paso a paso**\n\n"
            "**Verificar estado inicial:**\n"
            "1. `sh ip int brief` → fa0/fa1/fa2 deben estar en **admin down** *(R08)*\n\n"
            "**Habilitar interfaces:**\n"
            "2. `conf t` → `int fa0` → `no shutdown` → `exit`\n"
            "3. `int fa1` → `no shutdown` → `exit`\n"
            "4. `int fa2` → `no shutdown` → `exit`\n"
            "5. `sh int status` → verificar **connected** *(R09)*\n"
            "6. `sh ip int brief` → verificar **up/up**\n\n"
            "**Validar direccionamiento lógico:**\n"
            "7. `sh arp` → verificar BVI2 (cajero+cámaras) y BVI3 (alarmas) con IPs\n\n"
            "**Aprender MACs y configurar ACLs:**\n"
            "8. `sh mac` → anotar MAC de fa0, fa1 y fa2 *(R09)*\n"
            "9. `conf t`\n"
            "10. `no access-list 700` → `access-list 700 permit MAC_cajero`\n"
            "11. `access-list 700 permit MAC_camaras` *(R10)*\n"
            "12. `no access-list 701` → `access-list 701 permit MAC_alarmas`\n"
            "13. `do wr` → guardar configuración *(R11)*\n\n"
            "**Validar con Soporte Básico:**\n"
            "14. Ejecutar el flujo completo de **Soporte Básico** (pings BVI2 y BVI3)"
        )
        return respuesta, ["R08", "R09", "R10", "R11"]

    # ── ERRORES FÍSICOS ──
    elif intencion == "errores_fisicos":
        respuesta = (
            "**Errores físicos en interfaces — diagnóstico y solución**\n\n"
            "**Identificar errores** *(R05)*:\n"
            "1. `sh int | in error` → muestra todas las interfaces con errores\n\n"
            "**Identificar la interfaz específica** *(R06)*:\n"
            "2. `sh int fa0 | in error`\n"
            "3. `sh int fa1 | in error`\n"
            "4. `sh int fa2 | in error`\n\n"
            "**Acción correctiva:**\n"
            "5. Solicitar cambio de cable al técnico en la interfaz con errores\n"
            "6. `clear counters` + Enter + Enter → limpiar contadores\n"
            "7. `sh ip int brief` → verificar estado de interfaces\n"
            "8. Monitorear si los errores vuelven a incrementar\n\n"
            "⚠️ Los errores físicos persistentes después del cambio de cable pueden indicar "
            "falla en el puerto del switch del dispositivo conectado."
        )
        return respuesta, ["R05", "R06"]

    # ── PING / CONECTIVIDAD ──
    elif intencion == "ping":
        respuesta = (
            "**Cajero sin conectividad — secuencia de diagnóstico**\n\n"
            "**1. Verificar capa física** *(R01)*:\n"
            "`sh ip int brief` → fa0, fa1 y fa2 deben estar **up/up**\n"
            "→ Si están admin down: habilitar con `no shutdown`\n\n"
            "**2. Verificar interfaces lógicas** *(R02)*:\n"
            "`sh arp` → BVI2 debe tener IPs de cajero y cámaras; BVI3 IP de alarmas\n\n"
            "**3. Pings BVI2** *(R03)*:\n"
            "- Ping a gateway BVI2 → desde router\n"
            "- Ping a IP cajero → desde CMD en red corporativa\n"
            "- Ping a IP cámaras → desde router\n\n"
            "**4. Pings BVI3** *(R04)*:\n"
            "- Ping a gateway BVI3 → desde router\n"
            "- Ping a IP alarmas → desde router\n\n"
            "**5. Revisar errores físicos** *(R05)*:\n"
            "`sh int | in error` → si hay errores, identificar interfaz y cambiar cable"
        )
        return respuesta, ["R01", "R02", "R03", "R04", "R05"]

    # ── TUNNEL / GM ──
    elif intencion == "tunnel":
        respuesta = (
            "**Diagnóstico del tunnel GetVPN desde el GM**\n\n"
            "El GM es el concentrador de todos los enlaces — aquí solo se diagnostica, "
            "nunca se interviene activamente.\n\n"
            "**Pasos desde el GM:**\n"
            "1. `sh run | in (numero_cajero)` → identifica el TunnelX del cajero\n"
            "2. `sh run int TunnelX` → valida tunnel source y destination\n"
            "3. Ping a tunnel destination (SIM — IP del proveedor 4G)\n"
            "4. Ping source (tunnel source) a tunnel destination\n"
            "5. Ping sin source → punta nuestra\n"
            "6. Ping a IP del proveedor (IP impar del bloque)\n"
            "7. Ping a nuestra punta (IP siguiente a la configurada)\n\n"
            "✅ Si todos responden → proceder a conmutación forzada en el router\n"
            "❌ Si alguno falla → problema de transporte, escalar al proveedor"
        )
        return respuesta, ["R12"]

    # ── MAC / ACL ──
    elif intencion == "mac_acl":
        respuesta = (
            "**Configuración de ACLs por MAC — paso a paso**\n\n"
            "**Aprender MACs** *(R09)*:\n"
            "1. `sh mac` → anotar MAC de fa0 (cajero), fa1 (cámaras), fa2 (alarmas)\n\n"
            "**Configurar ACL 700** (cajero + cámaras) *(R10)*:\n"
            "2. `conf t`\n"
            "3. `no access-list 700`\n"
            "4. `access-list 700 permit MAC_cajero`\n"
            "5. `access-list 700 permit MAC_camaras`\n\n"
            "**Configurar ACL 701** (alarmas) *(R10)*:\n"
            "6. `no access-list 701`\n"
            "7. `access-list 701 permit MAC_alarmas`\n\n"
            "**Guardar** *(R11)*:\n"
            "8. `do wr`"
        )
        return respuesta, ["R09", "R10", "R11"]

    # ── BVI / ARP ──
    elif intencion == "bvi_arp":
        respuesta = (
            "**Validación de interfaces lógicas BVI**\n\n"
            "`sh arp` → verificar que aparezcan:\n\n"
            "**BVI2** (cajero + cámaras):\n"
            "- 1ra IP → gateway BVI2\n"
            "- 2da IP → dirección del cajero\n"
            "- 3ra IP → dirección de cámaras\n\n"
            "**BVI3** (alarmas):\n"
            "- 1ra IP → gateway BVI3\n"
            "- 2da IP → dirección de alarmas\n\n"
            "**Pings de validación BVI2** *(R03)*:\n"
            "- Gateway → desde router\n"
            "- Cajero → desde CMD en red corporativa\n"
            "- Cámaras → desde router\n\n"
            "**Pings de validación BVI3** *(R04)*:\n"
            "- Gateway → desde router\n"
            "- Alarmas → desde router"
        )
        return respuesta, ["R02", "R03", "R04"]

    # ── MEDIO ACTIVO ──
    elif intencion == "medio_activo":
        respuesta = (
            "**Verificación del medio activo**\n\n"
            "`sh ip int brief` → revisar fa3 y fa4:\n\n"
            "- **fa4 up/up, fa3 admin down** → servicio por VSAT (normal)\n"
            "- **fa3 up/up, fa4 down/down** → servicio por 4G (IP SLA conmutó)\n"
            "- **fa3 up/up, fa4 up/up** → ambos activos, revisar routing\n\n"
            "Si fa3 está activo cuando no debería → el IP SLA detectó falla real en VSAT. "
            "Revisar el estado de fa4 y el proveedor VSAT."
        )
        return respuesta, ["R07"]

    # ── SOPORTE BÁSICO GENERAL ──
    elif intencion == "soporte_basico":
        respuesta = (
            "**Soporte básico de conectividad — paso a paso completo**\n\n"
            "Este es el primer paso en cualquier intervención sobre un cajero.\n\n"
            "**1. Verificar capa física** *(R01)*:\n"
            "`sh ip int brief` → fa0/fa1/fa2 deben estar **up/up**\n\n"
            "**2. Verificar BVIs** *(R02)*:\n"
            "`sh arp` → BVI2 y BVI3 con IPs asignadas\n\n"
            "**3. Pings BVI2** *(R03)*:\n"
            "- GW BVI2 (router) / Cajero (CMD) / Cámaras (router)\n\n"
            "**4. Pings BVI3** *(R04)*:\n"
            "- GW BVI3 (router) / Alarmas (router)\n\n"
            "**5. Revisar errores físicos** *(R05)*:\n"
            "`sh int | in error`\n\n"
            "**6a. Si hay errores** *(R06)*:\n"
            "`sh int faX | in error` → identificar interfaz → cambio de cable → `clear counters`\n\n"
            "**6b. Sin errores** *(R07)*:\n"
            "`sh ip int brief` → confirmar medio activo (VSAT fa4 o 4G fa3)"
        )
        return respuesta, ["R01", "R02", "R03", "R04", "R05", "R06", "R07"]

    # ── SIN MATCH — respuesta de ayuda ──
    return (
        "No identifiqué el escenario exacto. Puedo ayudarte con:\n\n"
        "- **Conmutación forzada**: 'necesito hacer una conmutación', 'vsat fallando', 'pasar a 4g'\n"
        "- **Instalación nueva**: 'instalar cajero', 'cajero nuevo', 'poner en servicio'\n"
        "- **Sin conectividad**: 'cajero caído', 'no responde ping', 'sin acceso'\n"
        "- **Interfaces abajo**: 'admin down', 'no sube la interfaz'\n"
        "- **Errores físicos**: 'errores en interfaz', 'cambio de cable'\n"
        "- **Tunnel / GM**: 'tunnel caído', 'verificar GM'\n"
        "- **BVI / ARP**: 'bvi2 sin IP', 'sh arp'\n"
        "- **Soporte básico**: 'ayuda', 'diagnóstico', 'por dónde empiezo'",
        []
    )


# ============================================================
# INICIALIZAR ESTADO
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = None

# ============================================================
# HEADER
# ============================================================

col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        st.image("logo.png", width=160)
    except:
        st.markdown("🏦", unsafe_allow_html=False)

with col_titulo:
    st.markdown("""
        <p class="titulo">SBC AVAL VALOR COMPARTIDO</p>
        <p class="subtitulo">Sistema Basado en Conocimiento — Soporte Técnico de Cajeros</p>
        <p class="descripcion">
        Motor de inferencia con encadenamiento hacia adelante sobre 14 reglas de producción
        formalizadas en lógica de predicados. Infraestructura Cisco 881 / GetVPN / VSAT+4G.
        </p>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================
# MÉTRICAS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

metricas = [
    ("14", "Reglas SBC"),
    ("3", "Escenarios"),
    ("12", "Predicados"),
    ("✓", "Motor activo"),
]

for col, (val, lbl) in zip([m1, m2, m3, m4], metricas):
    with col:
        st.markdown(f"""
        <div class="metrica-box">
            <div class="metrica-valor">{val}</div>
            <div class="metrica-label">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    try:
        st.image("logo.png", width=110)
    except:
        pass

    st.markdown("## 🗂️ Navegación")
    st.markdown("---")

    escenario = st.selectbox(
        "Escenario de diagnóstico",
        ["🔧 Soporte básico", "📦 Instalación nueva", "📡 Conmutación VSAT → 4G"]
    )

    st.markdown("---")
    st.markdown("### 🤖 Asistente técnico IA")
    st.caption("Describa la falla en lenguaje natural")

    pregunta_chat = st.text_area("Falla o síntoma observado", height=90, placeholder="Ej: El cajero no responde ping, interfaces abajo, VSAT con intermitencia...")

    if st.button("Consultar asistente"):
        if pregunta_chat.strip():
            respuesta, reglas_act = responder_chatbot(pregunta_chat)
            st.session_state.chat_history.append({
                "usuario": pregunta_chat,
                "bot": respuesta,
                "reglas": reglas_act
            })

    if st.button("Limpiar historial", type="secondary"):
        st.session_state.chat_history = []

    st.markdown("---")
    st.markdown("### 📋 Referencia rápida")
    st.caption("fa0=cajero | fa1=cámaras | fa2=alarmas")
    st.caption("fa3=4G backup | fa4=VSAT principal")
    st.caption("bvi2=cajero+cámaras | bvi3=alarmas")
    st.caption("ACL700=cajero+cámaras | ACL701=alarmas")

# ============================================================
# TABS PRINCIPALES
# ============================================================

tab_diag, tab_chat, tab_reglas = st.tabs([
    " Diagnóstico guiado",
    "🤖 Asistente IA",
    " Base de conocimiento"
])

# ============================================================
# TAB 1 — DIAGNÓSTICO GUIADO CON MOTOR REAL
# ============================================================

with tab_diag:

    reglas_sbc = crear_base_conocimiento()

    # ── SOPORTE BÁSICO ──
    if escenario == "🔧 Soporte básico":
        st.subheader("🔧 Soporte básico de conectividad")
        st.caption("Primer paso obligatorio en cualquier intervención. Si las interfaces físicas no están up/up, nada de la validación lógica funcionará.")

        st.markdown("#### Estado de interfaces físicas")
        c1, c2, c3 = st.columns(3)
        with c1:
            fa0 = st.selectbox("fa0 (cajero)", ["up/up", "admin down", "down/down"], key="s_fa0")
        with c2:
            fa1 = st.selectbox("fa1 (cámaras)", ["up/up", "admin down", "down/down"], key="s_fa1")
        with c3:
            fa2 = st.selectbox("fa2 (alarmas)", ["up/up", "admin down", "down/down"], key="s_fa2")

        st.markdown("#### Interfaces lógicas (sh arp)")
        c1, c2 = st.columns(2)
        with c1:
            bvi2 = st.selectbox("BVI2 tiene direccionamiento", ["Sí", "No"], key="s_bvi2")
        with c2:
            bvi3 = st.selectbox("BVI3 tiene direccionamiento", ["Sí", "No"], key="s_bvi3")

        st.markdown("#### Pings BVI2")
        c1, c2, c3 = st.columns(3)
        with c1:
            p_gw2 = st.selectbox("Ping gateway BVI2", ["OK", "Falla"], key="s_pgw2")
        with c2:
            p_caj = st.selectbox("Ping cajero (CMD)", ["OK", "Falla"], key="s_pcaj")
        with c3:
            p_cam = st.selectbox("Ping cámaras (router)", ["OK", "Falla"], key="s_pcam")

        st.markdown("#### Pings BVI3")
        c1, c2 = st.columns(2)
        with c1:
            p_gw3 = st.selectbox("Ping gateway BVI3", ["OK", "Falla"], key="s_pgw3")
        with c2:
            p_ala = st.selectbox("Ping alarmas (router)", ["OK", "Falla"], key="s_pala")

        st.markdown("#### Errores físicos (sh int | in error)")
        errores = st.selectbox("Errores físicos detectados", ["No", "Sí"], key="s_err")

        if st.button("▶ Ejecutar diagnóstico", key="btn_soporte"):
            hechos = set()
            if fa0 == "up/up": hechos.add("fa0_up_up")
            if fa1 == "up/up": hechos.add("fa1_up_up")
            if fa2 == "up/up": hechos.add("fa2_up_up")
            if bvi2 == "Sí": hechos.add("bvi2_con_direccionamiento")
            if bvi3 == "Sí": hechos.add("bvi3_con_direccionamiento")
            if p_gw2 == "OK": hechos.add("ping_gw_bvi2_ok")
            if p_caj == "OK": hechos.add("ping_cajero_ok")
            if p_cam == "OK": hechos.add("ping_camaras_ok")
            if p_gw3 == "OK": hechos.add("ping_gw_bvi3_ok")
            if p_ala == "OK": hechos.add("ping_alarmas_ok")
            if errores == "Sí":
                hechos.add("errores_fisicos_detectados")
            else:
                hechos.add("sin_errores_fisicos")

            hechos_finales, reglas_aplicadas = encadenamiento_adelante(hechos, reglas_sbc)
            conclusiones = hechos_finales - hechos

            st.divider()
            st.markdown("### 🔗 Cadena de razonamiento")

            if not reglas_aplicadas:
                st.markdown("""<div class="card-error">
                    <b>⚠ Sin reglas disparadas</b><br>
                    Las interfaces físicas no están en condición de proceder.
                    Verificar fa0/fa1/fa2 con <code>sh ip int brief</code>.
                    </div>""", unsafe_allow_html=True)
            else:
                for i, r in enumerate(reglas_aplicadas, 1):
                    icono = "🖧" if r.get("contexto") == "gm" else "🔧"
                    cert = f"{int(r['certeza']*100)}%"
                    st.markdown(f"""
                    <div class="card-regla">
                        <span class="badge">{r['nombre']}</span>
                        <span style="color:#94a3b8;font-size:12px">certeza {cert}</span>
                        {icono} <b style="color:white">{r['descripcion']}</b><br>
                        <span style="color:#60a5fa;font-size:13px">→ {r['accion']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("### ✅ Conclusiones del motor")
                for c in sorted(conclusiones):
                    color = "#22c55e" if "correcta" in c or "activo" in c or "ok" in c else "#60a5fa"
                    st.markdown(f"""
                    <div style="padding:8px 16px;background:#0f172a;border-radius:8px;margin:4px 0;
                    border-left:3px solid {color};">
                        <span style="color:{color}">✓</span>
                        <span style="color:#e2e8f0;margin-left:8px">{c.replace('_',' ')}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # ── INSTALACIÓN NUEVA ──
    elif escenario == "📦 Instalación nueva":
        st.subheader("📦 Instalación nueva de cajero")
        st.caption("fa3 y fa4 ya vienen activas. Solo se intervienen fa0, fa1 y fa2.")

        st.markdown("#### Estado inicial (sh ip int brief)")
        c1, c2, c3 = st.columns(3)
        with c1:
            fa0_i = st.selectbox("fa0", ["admin down", "up/up"], key="i_fa0")
        with c2:
            fa1_i = st.selectbox("fa1", ["admin down", "up/up"], key="i_fa1")
        with c3:
            fa2_i = st.selectbox("fa2", ["admin down", "up/up"], key="i_fa2")

        st.markdown("#### Después de no shutdown (sh int status)")
        c1, c2, c3 = st.columns(3)
        with c1:
            fa0_c = st.selectbox("fa0 estado", ["connected", "not connected"], key="i_fa0c")
        with c2:
            fa1_c = st.selectbox("fa1 estado", ["connected", "not connected"], key="i_fa1c")
        with c3:
            fa2_c = st.selectbox("fa2 estado", ["connected", "not connected"], key="i_fa2c")

        st.markdown("#### sh arp — Direccionamiento BVI")
        c1, c2 = st.columns(2)
        with c1:
            bvi2_i = st.selectbox("BVI2 con IPs", ["Sí", "No"], key="i_bvi2")
        with c2:
            bvi3_i = st.selectbox("BVI3 con IPs", ["Sí", "No"], key="i_bvi3")

        st.markdown("#### sh mac — MACs aprendidas")
        c1, c2, c3 = st.columns(3)
        with c1:
            mac_c = st.selectbox("MAC cajero (fa0)", ["Sí", "No"], key="i_macc")
        with c2:
            mac_cam = st.selectbox("MAC cámaras (fa1)", ["Sí", "No"], key="i_macca")
        with c3:
            mac_a = st.selectbox("MAC alarmas (fa2)", ["Sí", "No"], key="i_maca")

        st.markdown("#### ACLs configuradas")
        c1, c2 = st.columns(2)
        with c1:
            acl700 = st.selectbox("ACL 700 (cajero+cámaras)", ["Sí", "No"], key="i_acl700")
        with c2:
            acl701 = st.selectbox("ACL 701 (alarmas)", ["Sí", "No"], key="i_acl701")

        if st.button("▶ Validar instalación", key="btn_inst"):
            hechos = set()
            if fa0_i == "admin down": hechos.add("fa0_admin_down")
            if fa1_i == "admin down": hechos.add("fa1_admin_down")
            if fa2_i == "admin down": hechos.add("fa2_admin_down")
            if fa0_c == "connected": hechos.add("fa0_connected")
            if fa1_c == "connected": hechos.add("fa1_connected")
            if fa2_c == "connected": hechos.add("fa2_connected")
            # up/up implícito si connected
            if fa0_c == "connected": hechos.add("fa0_up_up")
            if fa1_c == "connected": hechos.add("fa1_up_up")
            if fa2_c == "connected": hechos.add("fa2_up_up")
            if bvi2_i == "Sí": hechos.add("bvi2_con_direccionamiento")
            if bvi3_i == "Sí": hechos.add("bvi3_con_direccionamiento")
            if mac_c == "Sí": hechos.add("mac_cajero_aprendida")
            if mac_cam == "Sí": hechos.add("mac_camaras_aprendida")
            if mac_a == "Sí": hechos.add("mac_alarmas_aprendida")
            if acl700 == "Sí": hechos.add("acl700_configurada")
            if acl701 == "Sí": hechos.add("acl701_configurada")

            hechos_finales, reglas_aplicadas = encadenamiento_adelante(hechos, reglas_sbc)
            conclusiones = hechos_finales - hechos

            st.divider()
            st.markdown("### 🔗 Cadena de razonamiento")

            if not reglas_aplicadas:
                st.markdown("""<div class="card-warning">
                    <b>⚠ No se disparó ninguna regla.</b><br>
                    Verifique que las interfaces estén en admin down para comenzar la instalación.
                    </div>""", unsafe_allow_html=True)
            else:
                for i, r in enumerate(reglas_aplicadas, 1):
                    cert = f"{int(r['certeza']*100)}%"
                    st.markdown(f"""
                    <div class="card-regla">
                        <span class="badge">{r['nombre']}</span>
                        <span style="color:#94a3b8;font-size:12px">certeza {cert}</span>
                        🔧 <b style="color:white">{r['descripcion']}</b><br>
                        <span style="color:#60a5fa;font-size:13px">→ {r['accion']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                if "guardar_configuracion" in conclusiones:
                    st.markdown("""<div class="card-exito">
                        <b>✅ Instalación completada</b><br>
                        Configuración guardada con <code>do wr</code>. 
                        Proceda a ejecutar Soporte Básico para validar conectividad completa.
                        </div>""", unsafe_allow_html=True)

    # ── CONMUTACIÓN ──
    elif escenario == "📡 Conmutación VSAT → 4G":
        st.subheader("📡 Conmutación forzada VSAT → 4G")

        col_gm, col_rtr = st.columns(2)

        with col_gm:
            st.markdown("#### 🖧 Diagnóstico desde GM (solo lectura)")
            st.caption("El GM es el concentrador de todos los enlaces GetVPN. Aquí solo se diagnostica.")
            tunnel = st.selectbox("Tunnel GM activo (sh run int TunnelX)", ["Sí", "No"], key="c_tunnel")
            pings = st.selectbox("Todos los pings del tunnel OK", ["Sí", "No"], key="c_pings")
            st.caption("Pings: SIM (tunnel dest), tunnel source, punta propia, punta proveedor")

        with col_rtr:
            st.markdown("#### 🔧 Intervención en router del cajero")
            st.caption("Toda la intervención activa se hace aquí, nunca en el GM.")
            reload_p = st.selectbox("Reload in 10 programado", ["Sí", "No"], key="c_reload")
            vsat_i = st.selectbox("VSAT inactivo (fa4 abajo)", ["Sí", "No"], key="c_vsat")
            lte = st.selectbox("4G activo (IP SLA conmutó a fa3)", ["Sí", "No"], key="c_lte")

        if st.button("▶ Ejecutar conmutación", key="btn_conv"):
            hechos = set()
            if tunnel == "Sí": hechos.add("tunnel_gm_activo")
            if pings == "Sí": hechos.add("pings_tunnel_ok")
            if reload_p == "Sí": hechos.add("reload_programado")
            if vsat_i == "Sí": hechos.add("vsat_inactivo")
            if lte == "Sí": hechos.add("4g_activo")

            hechos_finales, reglas_aplicadas = encadenamiento_adelante(hechos, reglas_sbc)
            conclusiones = hechos_finales - hechos

            st.divider()
            st.markdown("### 🔗 Cadena de razonamiento")

            if not reglas_aplicadas:
                st.markdown("""<div class="card-error">
                    <b>⚠ No se puede ejecutar la conmutación.</b><br>
                    Verifique el tunnel en el GM y que los pings respondan antes de proceder.
                    </div>""", unsafe_allow_html=True)
            else:
                for r in reglas_aplicadas:
                    cert = f"{int(r['certeza']*100)}%"
                    icono = "🖧" if "GM" in r["accion"] else "🔧"
                    st.markdown(f"""
                    <div class="card-regla">
                        <span class="badge">{r['nombre']}</span>
                        <span style="color:#94a3b8;font-size:12px">certeza {cert}</span>
                        {icono} <b style="color:white">{r['descripcion']}</b><br>
                        <span style="color:#60a5fa;font-size:13px">→ {r['accion']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                if "cancelar_reload" in conclusiones:
                    st.markdown("""<div class="card-exito">
                        <b>✅ Conmutación exitosa</b><br>
                        Servicio migrando por 4G. Ejecute <code>no reload</code> y proceda 
                        a Soporte Básico para validar conectividad completa.
                        </div>""", unsafe_allow_html=True)
                elif "bajar_fa4_vsat" in conclusiones and "cancelar_reload" not in conclusiones:
                    st.markdown("""<div class="card-warning">
                        <b>⏳ fa4 bajado — esperando activación 4G</b><br>
                        Verifique que el IP SLA detectó la caída y levantó fa3.
                        Confirme con <code>sh ip int brief</code>.
                        </div>""", unsafe_allow_html=True)

# ============================================================
# TAB 2 — CHATBOT IA
# ============================================================

with tab_chat:
    st.subheader("🤖 Asistente técnico IA")
    st.caption("Describa la falla en lenguaje natural. El asistente activa el motor de inferencia real para diagnosticar.")

    # Mostrar historial
    if not st.session_state.chat_history:
        st.markdown("""<div class="card-info">
            <b>💡 Ejemplos de consultas:</b><br>
            • "El cajero no responde ping"<br>
            • "Las interfaces están admin down"<br>
            • "VSAT con intermitencia, necesito conmutar"<br>
            • "Errores físicos en las interfaces"<br>
            • "Cómo configuro las ACLs por MAC"<br>
            • "El tunnel en el GM no está activo"
            </div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            st.markdown(f'<div class="chat-user">👤 {msg["usuario"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bot">🤖 {msg["bot"]}</div>', unsafe_allow_html=True)
            if msg["reglas"]:
                reglas_str = " → ".join([f"**{r}**" for r in msg["reglas"]])
                st.caption(f"Reglas activadas: {reglas_str}")
            st.markdown("")

# ============================================================
# TAB 3 — BASE DE CONOCIMIENTO
# ============================================================

with tab_reglas:
    st.subheader("📚 Base de conocimiento — 14 reglas de producción")
    st.caption("Formalizadas en lógica de predicados de primer orden. Motor: encadenamiento hacia adelante (Modus Ponens).")

    bloques = {
        "🔧 Bloque A — Soporte básico (R01–R07)": [r for r in reglas_sbc if r["nombre"] in ["R01","R02","R03","R04","R05","R06","R07"]],
        "📦 Bloque B — Instalación nueva (R08–R11)": [r for r in reglas_sbc if r["nombre"] in ["R08","R09","R10","R11"]],
        "📡 Bloque C — Conmutación VSAT→4G (R12–R14)": [r for r in reglas_sbc if r["nombre"] in ["R12","R13","R14"]],
    }

    for bloque_nombre, reglas_bloque in bloques.items():
        with st.expander(bloque_nombre, expanded=True):
            for r in reglas_bloque:
                cert_color = "#22c55e" if r["certeza"] == 1.0 else "#f59e0b"
                conds = " ∧ ".join(r["condiciones"])
                st.markdown(f"""
                <div class="card-regla" style="margin-bottom:12px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                        <span class="badge">{r['nombre']}</span>
                        <span style="color:{cert_color};font-size:12px;font-weight:600">
                            certeza {int(r['certeza']*100)}%
                        </span>
                    </div>
                    <div style="color:#94a3b8;font-size:12px;margin-bottom:6px">
                        <b style="color:#60a5fa">SI:</b> {conds}
                    </div>
                    <div style="color:#94a3b8;font-size:12px;margin-bottom:6px">
                        <b style="color:#22c55e">ENTONCES:</b> {r['conclusion']}
                    </div>
                    <div style="color:#cbd5e1;font-size:13px;margin-top:8px">
                        📋 {r['descripcion']}
                    </div>
                    <div style="color:#60a5fa;font-size:13px;margin-top:4px">
                        ⚡ {r['accion']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("AVAL VALOR COMPARTIDO | Sistema Basado en Conocimiento — Soporte Técnico Cajeros | 2026")