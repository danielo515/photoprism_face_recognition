import * as state from './appState';
import { toolbar } from './toolbar';

export const removeFacesFromDOM = (ids) => {
    ids.forEach((id) => document.getElementById(id).parentElement.remove());
};

export const selectFace = (evt) => {
    const node = evt.currentTarget;
    const data = node.dataset;
    const id = node.id;
    const url = node.style.backgroundImage.replace(/url..([^"]*).*/, '$1');
    const classList = node.classList;
    if (state.toggleFace({ id, url }) === 'removed') {
        classList.remove('selected');
    } else {
        node.classList.add('selected');
    }
    toolbar();
};

export const clearSelection = () => {
    document
        .querySelectorAll('.selected')
        .forEach((node) => node.classList.remove('selected'));
    state.clearFaces();
    toolbar();
};
