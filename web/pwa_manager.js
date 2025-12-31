/**
 * PWA Manager
 * 
 * Handles service worker registration and PWA installation prompts.
 */

export function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('service-worker.js')
                .then((registration) => {
                    console.log('ServiceWorker registration successful with scope: ', registration.scope);

                    // Check for updates periodically
                    setInterval(() => {
                        registration.update();
                    }, 60 * 60 * 1000); // Check every hour
                })
                .catch((error) => {
                    console.warn('ServiceWorker registration failed:', error);
                });
        });
    }
}

export function initInstallPrompt() {
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome 67 and earlier from automatically showing the prompt
        e.preventDefault();
        // Stash the event so it can be triggered later.
        deferredPrompt = e;

        // Optionally, show a custom install button in your UI
        const installBtn = document.createElement('button');
        installBtn.id = 'install-btn';
        installBtn.className = 'btn btn-secondary';
        installBtn.style.position = 'fixed';
        installBtn.style.bottom = '20px';
        installBtn.style.right = '20px';
        installBtn.style.zIndex = '1000';
        installBtn.innerHTML = '✨ Install App';

        installBtn.addEventListener('click', async () => {
            if (!deferredPrompt) return;

            // Show the prompt
            deferredPrompt.prompt();
            // Wait for the user to respond to the prompt
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User ${outcome} the install prompt`);

            deferredPrompt = null;
            installBtn.remove();
        });

        document.body.appendChild(installBtn);
    });

    window.addEventListener('appinstalled', () => {
        console.log('PWA installed successfully');
        const installBtn = document.getElementById('install-btn');
        if (installBtn) installBtn.remove();
    });
}
