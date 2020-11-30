import { selectFace } from './actions';
import modal from './modal';
import './styles/index.scss';
import configPage from './configPage';

window.selectFace = selectFace;

modal({ isOpen: false, content: 'I am just a modal' });

if (window.page === 'config') {
    console.log(window.server_data);
    configPage(document.getElementById('config'), window.server_data);
}
