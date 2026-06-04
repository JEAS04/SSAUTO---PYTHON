# Generador de Mensajes de Contacto - Documentación

## 📋 Descripción General

Se ha implementado un **generador de mensajes de contacto** moderno y funcional utilizando `customtkinter`, que permite crear mensajes estandarizados para tres situaciones comunes de contacto con clientes.

## 🎯 Características Principales

### 1. **Tipos de Mensaje Disponibles**
- **Fuera de Servicio**: Para cuando el número registrado está fuera de servicio
- **Buzón de Voz**: Para cuando la llamada es dirigida al buzón de voz
- **No Contesta**: Para cuando el cliente no responde la llamada

### 2. **Soporte Bilingüe**
- Español (por defecto)
- Inglés
- Cada tipo de mensaje tiene su propia traducción profesional

### 3. **Manejo Inteligente de Números Telefónicos**
- Permite ingresar **1 o 2 números telefónicos**
- **Detección automática de singular/plural**:
  - 1 número: "al número", "el número", "fue enviado"
  - 2 números: "a los números", "los números", "fueron enviados"
- Los números se muestran automáticamente en el mensaje generado

### 4. **Fecha Automática**
- Formato: `MM/DD/YYYY` (ej: 05/25/2026)
- Se genera automáticamente al crear el mensaje
- Solo se incluye en las plantillas en inglés (como requiere el formato "LS:")

### 5. **Interfaz Moderna y Responsive**
- Diseño limpio y profesional con `customtkinter`
- Previsualización en tiempo real del mensaje
- Botones claramente identificados con emojis
- Confirmación visual al copiar el mensaje

## 🏗️ Arquitectura de la Solución

### **Decisión de Diseño: Mantener Separación**

Después de analizar `ventana_plantillas.py` y `template_filler.py`, se decidió:

1. **NO combinar** los archivos existentes
2. **Crear un nuevo módulo** (`ui/ventana_generador_mensajes.py`) específico para estos mensajes
3. **Mantener compatibilidad** con la funcionalidad existente

### **Razones de esta decisión:**

- `ventana_plantillas.py`: Gestiona plantillas genéricas editables con CRUD completo
- `template_filler.py`: Es un script standalone para plantillas con placeholders variables
- **Nuevo generador**: Casos específicos de contacto con lógica especializada (singular/plural, fecha automática)

### **Reutilización de Patrones:**
- Se mantuvo el patrón de `CTkToplevel` de `ventana_plantillas.py`
- Se reutilizó la función de copiar al portapapeles
- Se mantuvo el estilo visual consistente con la aplicación principal

## 📁 Estructura de Archivos

```
ssauto/
├── ui/
│   ├── ventana_generador_mensajes.py  ← NUEVO ARCHIVO
│   ├── ventana_plantillas.py          ← SIN CAMBIOS
│   └── ...
├── template_filler.py                 ← SIN CAMBIOS
├── main.py                            ← MODIFICADO (se agregó botón)
└── ...
```

## 🚀 Cómo Usar

### **1. Abrir el Generador**
- Ejecutar `main.py`
- Hacer clic en el botón **"Mensajes"** en la barra superior

### **2. Configurar el Mensaje**
1. **Seleccionar tipo de mensaje** (Fuera de Servicio, Buzón de Voz, No Contesta)
2. **Elegir idioma** (Español o English)
3. **Ingresar números telefónicos**:
   - Número 1 (obligatorio)
   - Número 2 (opcional, máximo 2 números)

### **3. Previsualizar y Copiar**
- El mensaje se genera **automáticamente** mientras escribes
- Revisar la previsualización
- Hacer clic en **"📋 Copiar Mensaje"**

## 💡 Ejemplos de Uso

### **Ejemplo 1: Un número - Fuera de Servicio (Español)**
```
Número 1: 555-1234
Resultado:
"Se llamó al número 555-1234, pero está fuera de servicio. Se envió un correo electrónico como método de contacto alternativo."
```

### **Ejemplo 2: Dos números - No Contesta (Español)**
```
Número 1: 555-1234
Número 2: 555-5678
Resultado:
"Se llamó a los clientes a los números 555-1234 y 555-5678, pero no respondió. Como alternativa de contacto, se envió un mensaje de texto y un correo electrónico."
```

### **Ejemplo 3: Un número - Buzón de Voz (Inglés)**
```
Número 1: 555-1234
Resultado:
"LS: 05/25/2026 The customer was called at the registered number, but the call went to voicemail. A text message and an email were sent."
```

## 🔧 Detalles Técnicos

### **Manejo de Singular/Plural**

El sistema usa una expresión regular para detectar patrones `{singular|plural}`:

```python
def _procesar_texto(plantilla, cantidad_numeros, telefonos_str, idioma):
    # Reemplaza {al número|a los números} según cantidad
    # Si cantidad == 1 → usa "al número"
    # Si cantidad == 2 → usa "a los números"
```

### **Validaciones**
- ✅ Mínimo 1 número telefónico
- ✅ Máximo 2 números telefónicos
- ✅ Mensaje de error si no hay números
- ✅ Mensaje de error si excede el límite

### **Plantillas**

Las plantillas están definidas en el diccionario `PLANTILLAS_MENSAJES`:

```python
PLANTILLAS_MENSAJES = {
    "fuera_servicio": {
        "titulo": "Fuera de Servicio",
        "es": "Se llamó {al número|a los números} {telefonos}, ...",
        "en": "LS: {fecha} A call was placed to the registered phone {number|numbers}, ..."
    },
    # ... más plantillas
}
```

## ✅ Compatibilidad y Mantenimiento

### **Lo que NO se rompió:**
- ✅ `ventana_plantillas.py` sigue funcionando igual
- ✅ `template_filler.py` sigue funcionando igual
- ✅ Todos los imports existentes se mantienen
- ✅ El estilo visual es consistente
- ✅ La aplicación principal (`main.py`) funciona correctamente

### **Buenas Prácticas Aplicadas:**
- ✅ Código modular y fácil de mantener
- ✅ Comentarios claros en español
- ✅ Nombres de variables descriptivos
- ✅ Separación de responsabilidades
- ✅ Manejo de errores básico
- ✅ Sin código redundante

## 🔄 Flujo de Trabajo Recomendado

1. **Para mensajes de contacto estandarizados** → Usar **Generador de Mensajes**
2. **Para plantillas personalizables** → Usar **Plantillas** (ventana_plantillas.py)
3. **Para mensajes con placeholders variables** → Usar **Template Filler** (template_filler.py)

## 📝 Notas Importantes

- El generador está diseñado específicamente para los 3 tipos de mensajes de contacto
- Los mensajes se copian al portapapeles listos para pegar
- La fecha se genera automáticamente en el momento de crear el mensaje
- El formato de fecha (MM/DD/YYYY) es el estándar americano

## 🎨 Características de UI/UX

- **Diseño moderno** con customtkinter
- **Responsive** dentro de las limitaciones de customtkinter
- **Iconos emoji** para mejor identificación visual
- **Feedback visual** al copiar (mensaje de confirmación)
- **Previsualización en tiempo real** mientras se escriben los números
- **Organización clara** por secciones (configuración, teléfonos, preview)

## 🔮 Posibles Mejoras Futuras

- Agregar más tipos de mensajes si se requieren
- Permitir personalizar las plantillas (guardar en JSON)
- Agregar historial de mensajes generados
- Exportar a diferentes formatos
- Integrar con APIs de envío de mensajes

---

**Implementado el**: 2026-05-25  
**Versión**: 0.1.1  
**Autor**: SSAuto Development Team