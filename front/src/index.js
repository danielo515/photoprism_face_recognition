import { selectFace } from './actions';
import modal from './Modal';
import './styles/index.scss';
import configPage from './configPage';
import { bind } from 'hyperhtml';
import { Suggestions } from './NewPerson';
import { getFacesMatches } from './api';

window.selectFace = selectFace;

modal({ isOpen: false, content: 'I am just a modal' });

if (window.page === 'config') {
    configPage(document.getElementById('config'), window.server_data);
}

if (window.page === 'person-faces') {
    const faceIds = window.server_data.faces.map((f) => f.id);
    const root = bind(document.getElementById('possible-matches'));
    getFacesMatches({ ids: faceIds }).then(
        ({ faces }) => root`${Suggestions({ faces })}`,
    );
}
