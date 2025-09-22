class AutoCloseByWords {
    constructor(selector, config = {}) {
      this.element = document.querySelector(selector);
      if (!this.element) return;

      const texto = this.element.textContent || '';
      const palabras = texto.trim().split(/\s+/).length;

      // Configuración con valores por defecto
      const {
        ratio = 1000,       // milisegundos por X palabras
        cadaPalabras = 5,   // cada cuántas palabras se suma el ratio
        min = 5000,         // mínimo 5 segundos
        max = 30000         // máximo 30 segundos
      } = config;

      const tiempo = Math.min(
        Math.max((palabras / cadaPalabras) * ratio, min),
        max
      );

      this.iniciar(tiempo);
    }

    iniciar(tiempo) {
      setTimeout(() => this.cerrar(), tiempo);
    }

    cerrar() {
      this.element.classList.remove('show');
      setTimeout(() => this.element.remove(), 500); // animación fade
    }
  }

  // Uso de la clase
  new AutoCloseByWords('#alerta-usuario');