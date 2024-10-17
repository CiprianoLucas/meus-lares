import { createApp, h } from 'vue';
import AlertPopup from './AlertPopup.vue';
import type {typesBootstrap} from './interfaces'
import { type AxiosError } from 'axios'
import { inputsLabel } from '@/components/inputs'

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

const resumeErrors = (error: AxiosError, defaultMessage: string = "Algo saiu errao") => {

    let errorMessage = ''
    if(error.response && error.response.data){
      const data = error.response.data as { [key: string]: string };
      Object.keys(inputsLabel).forEach(key => {
          if (data[key]){
              errorMessage += `${inputsLabel[key]}: ${data[key]}<br>`
          }})
    }
    if(!errorMessage && error.status === 404){
        return "Valor informado não foi encontrado"
    }
    return errorMessage?errorMessage:defaultMessage
}

export { popup, resumeErrors }