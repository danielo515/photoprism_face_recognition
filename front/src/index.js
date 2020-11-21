import { selectFace } from './App';
import modal from './modal';
import './styles/index.scss';

window.selectFace = selectFace;
console.log(window.selectFace);

modal({ isOpen: false, content: 'I am just a modal' });
