# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('agent.py', '.'),
        ('llm_client.py', '.'),
        ('alertas.py', '.'),
        ('conectividad.py', '.'),
        ('configuracion.py', '.'),
        ('encrypt_token.py', '.'),
        ('herramientas.py', '.'),
        ('informe.py', '.'),
        ('main.py', '.'),
        ('procesos.py', '.'),
        ('sistema.py', '.'),
        ('usuarios.py', '.'),
        ('wizard.py', '.'),
        ('__init__.py', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='agente',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    # Modo onedir (por defecto, no se especifica onefile)
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
