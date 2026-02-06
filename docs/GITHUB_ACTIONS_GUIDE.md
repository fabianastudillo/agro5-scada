# Guía para Generar Ejecutables con GitHub Actions

Este documento explica cómo usar GitHub Actions para compilar automáticamente ejecutables de Windows y Linux sin necesidad de tener ambos sistemas operativos.

## 🚀 Configuración Inicial

El workflow ya está configurado en `.github/workflows/build.yml`. No necesitas configurar nada adicional.

## 📦 Compilación Automática

### Compilar en cada Push

Simplemente haz `push` a las ramas `main` o `develop`:

```bash
git add .
git commit -m "Update application"
git push origin main
```

GitHub Actions automáticamente:
1. Compilará el ejecutable de Windows (en un runner Windows)
2. Compilará el ejecutable de Linux (en un runner Ubuntu)
3. Guardará ambos como artefactos durante 30 días

### Descargar los Ejecutables Compilados

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **"Actions"**
3. Selecciona el workflow más reciente (debe tener una marca verde ✓)
4. Desplázate hasta la sección **"Artifacts"**
5. Descarga:
   - `agro5-scada-windows` → Contiene `Agro5-SCADA.exe`
   - `agro5-scada-linux` → Contiene `Agro5-SCADA`

## 🏷️ Crear Releases con Binarios

Para crear un release oficial con los binarios adjuntos:

```bash
# 1. Crear un tag con formato v*.*.* 
git tag v1.0.0 -m "Primera versión estable"

# 2. Publicar el tag
git push origin v1.0.0
```

Esto automáticamente:
- ✅ Compila ambos ejecutables
- ✅ Crea un Release en GitHub
- ✅ Adjunta los binarios al Release
- ✅ Genera notas del release basadas en commits

El release estará disponible en:
```
https://github.com/TU_USUARIO/agro5-scada/releases
```

## 🔄 Compilación Manual (On-Demand)

Puedes disparar una compilación manualmente sin hacer push:

1. Ve a **Actions** en GitHub
2. Selecciona el workflow **"Build Executables"**
3. Haz clic en **"Run workflow"**
4. Selecciona la rama y haz clic en **"Run workflow"**

## 📊 Estados del Workflow

- ✅ **Verde (Success)**: Compilación exitosa, artefactos disponibles
- 🟡 **Amarillo (In Progress)**: Compilando...
- ❌ **Rojo (Failed)**: Error en compilación, revisar logs

## 🐛 Solución de Problemas

### Error: "PyQt6 no se puede instalar"

Si falla en Windows, puede ser por falta de dependencias. El workflow ya incluye la instalación completa.

### Los artefactos no aparecen

Asegúrate de que el workflow completó exitosamente (marca verde). Los artefactos solo se guardan si el build fue exitoso.

### El Release no se creó

Verifica:
- El tag debe empezar con `v` (ej: `v1.0.0`, no `1.0.0`)
- Ambos builds (Windows y Linux) deben completarse exitosamente

## 💡 Tips

1. **Commits frecuentes**: Cada push compila automáticamente, úsalo para probar
2. **Tags para versiones estables**: Solo crea tags cuando tengas una versión lista para distribuir
3. **Descarga desde Releases**: Los releases son permanentes, los artefactos expiran en 30 días
4. **Revisa los logs**: Si algo falla, los logs en Actions te dirán exactamente qué pasó

## 📝 Versionado Semántico

Recomendación para tags:

- `v1.0.0` - Primera versión estable
- `v1.1.0` - Nueva funcionalidad (backward compatible)
- `v1.1.1` - Corrección de bugs
- `v2.0.0` - Cambios que rompen compatibilidad

## 🔗 Enlaces Útiles

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Semantic Versioning](https://semver.org/)
