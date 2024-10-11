import { createApp, h } from 'vue';
import AlertPopup from './AlertPopup.vue';
import type {typesBootstrap} from './interfaces'

const popup = (title: string, message: string, type: typesBootstrap = 'success', time: number = 3000) => {
    const popupContainer = document.createElement('div');
    document.body.appendChild(popupContainer);

    const alertInstance = h(AlertPopup, {
		title: title,
		message: message,
		type: type,
		time: time
    });

    const app = createApp(alertInstance);
    app.mount(popupContainer);

    setTimeout(() => {
		app.unmount();
		popupContainer.remove();
    }, time + 1000);
};

export { popup }