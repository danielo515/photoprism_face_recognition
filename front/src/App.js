import { appState } from './appState';
import { toolbar } from './toolbar';

export const removeFacesFromDOM = (ids) => {
    ids.forEach((id) => document.getElementById(id).parentElement.remove());
};

export const selectFace = (evt) => {
    const node = evt.currentTarget;
    const data = node.dataset;
    const id = node.id;
    const classList = node.classList;
    if (appState.selectedFaces.has(id)) {
        classList.remove('selected');
        appState.selectedFaces.delete(id);
    } else {
        node.classList.add('selected');
        appState.selectedFaces.add(id);
    }
    toolbar();
};

export const clearSelection = () => {
    document
        .querySelectorAll('.selected')
        .forEach((node) => node.classList.remove('selected'));
    appState.selectedFaces.clear();
};
