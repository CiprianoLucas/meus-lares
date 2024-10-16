import { createApp, h } from 'vue';
import AlertPopup from './AlertPopup.vue';
import type {typesBootstrap} from './interfaces'
import { type AxiosError } from 'axios'

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

const resumeErrors = (error: AxiosError, inputs: { [key: string]: string }) => {
    let errorMessage = ''
    if(error.response && error.response.data){
      const data = error.response.data as { [key: string]: string };
      Object.keys(inputs).forEach(key => {
          if (data[key]){
              errorMessage += `${inputs[key]}: ${data[key]}<br>`
          }})
    }
    debugger
    if(!errorMessage && error.status === 404){
        return "Valor informado não foi encontrado"
    }
    return errorMessage?errorMessage:"Algo saiu errado"
}

export { popup, resumeErrors }