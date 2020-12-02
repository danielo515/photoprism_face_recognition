import { bind } from 'hyperhtml';

export const toggleClass = (id, className) => {
    const classes = document.getElementById(id).classList;
    classes.toggle(className);
};

export const getCoords = (x) => {
    return JSON.parse(x.dataset.coord);
};

const markFaces = () => {
    const facesDom = document.querySelector('.crop-face');
    const pos = getCoords(facesDom);
    bind(facesDom)`<div class='face-square' style=${{
        top: pos.top,
        left: pos.left,
    }} ></div>`;
    return facesDom;
};
