import { selectFace } from './App';
import modal from './modal';
import './styles/index.scss';
import configPage from './configPage';

window.selectFace = selectFace;
console.log(window.selectFace);

modal({ isOpen: false, content: 'I am just a modal' });

if (window.page === 'config') {
    console.log(window.server_data);
    configPage(document.getElementById('config'), window.server_data);
}
