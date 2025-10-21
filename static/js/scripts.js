console.log("JS cargado correctamente");

// --- Función para cerrar notificaciones de Bulma (mensajes flash) ---
document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });

    // Validación de formularios

    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    // Expresión regular para letras y números nomas
    const soloAlfanumerico = /^[a-zA-Z0-9]+$/;

    function mostrarError(inputId, errorId, mensaje) {
        document.getElementById(inputId).classList.add('is-danger'); // Marca el input en rojo
        document.getElementById(errorId).textContent = mensaje; // Muestra el mensaje de error
    }

    function quitarError(inputId, errorId) {
        document.getElementById(inputId).classList.remove('is-danger'); // Quita la marca roja
        document.getElementById(errorId).textContent = ''; // Limpia el mensaje de error
    }


    // Validación del Formulario de LOGIN
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            let esValido = true;

            // Campos de login
            const usernameInput = document.getElementById('username-login');
            const passwordInput = document.getElementById('password-login');

            // Limpiar errores previos
            quitarError('username-login', 'username-login-error');
            quitarError('password-login', 'password-login-error');

            // Validar que usuario no esté vacío
            if (usernameInput.value.trim() === '') {
                mostrarError('username-login', 'username-login-error', 'El nombre de usuario es obligatorio.');
                esValido = false;
            }

            // Validar que contraseña no esté vacía
            if (passwordInput.value.trim() === '') {
                mostrarError('password-login', 'password-login-error', 'La contraseña es obligatoria.');
                esValido = false;
            }

            // Si algo no es válido, detenemos el envío del formulario
            if (!esValido) {
                event.preventDefault();
            }
        });
    }


    // Validación del Formulario de REGISTRO
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            let esValido = true;

            // Campos de registro
            const usernameInput = document.getElementById('username-register');
            const passwordInput = document.getElementById('password-register');
            const password2Input = document.getElementById('password2-register');

            // Limpiar errores previos
            quitarError('username-register', 'username-register-error');
            quitarError('password-register', 'password-register-error');
            quitarError('password2-register', 'password2-register-error');

            // Validar que usuario no esté vacío
            if (usernameInput.value.trim() === '') {
                mostrarError('username-register', 'username-register-error', 'El nombre de usuario es obligatorio.');
                esValido = false;
            } 
            // Validar que usuario sea solo alfanumérico
            else if (!soloAlfanumerico.test(usernameInput.value.trim())) {
                mostrarError('username-register', 'username-register-error', 'El usuario solo debe contener letras y números (sin espacios).');
                esValido = false;
            }

            // Validar que contraseña no esté vacía
            if (passwordInput.value.trim() === '') {
                mostrarError('password-register', 'password-register-error', 'La contraseña es obligatoria.');
                esValido = false;
            } 
            // Requiere contraseña más fuerte, mínimo 6 caracteres.
            else if (passwordInput.value.trim().length < 6) {
                 mostrarError('password-register', 'password-register-error', 'La contraseña debe tener al menos 6 caracteres.');
                 esValido = false;
            }

            // Validar que la confirmación de contraseña no esté vacía
            if (password2Input.value.trim() === '') {
                mostrarError('password2-register', 'password2-register-error', 'Debes repetir la contraseña.');
                esValido = false;
            } 
            // Validar que las contraseñas coincidan
            else if (passwordInput.value.trim() !== password2Input.value.trim()) {
                mostrarError('password2-register', 'password2-register-error', 'Las contraseñas no coinciden.');
                esValido = false;
            }

            // Si algo no es válido, detenemos el envío del formulario
            if (!esValido) {
                event.preventDefault();
            }
        });
    }

});