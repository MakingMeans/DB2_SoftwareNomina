document.addEventListener("DOMContentLoaded", () => {
    const toastElement = document.getElementById("toast-data");
    if (toastElement) {
        const message = toastElement.getAttribute("data-message");
        const success = toastElement.getAttribute("data-success") === "true";
        showToast(message, success);
    }
});

function showToast(message, success) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: success ? 2500 : 4000,
        timerProgressBar: true,
        background: '#f0f0f0',
        iconColor: success ? 'green' : 'red',
        customClass: {
            popup: 'colored-toast'
        }
    });

    Toast.fire({
        icon: success ? 'success' : 'error',
        title: message
    });
}
