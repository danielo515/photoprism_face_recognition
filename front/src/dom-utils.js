export const toggleClass = (id, className) => {
    const classes = document.getElementById(id).classList;
    classes.toggle(className);
};

export const getCoords = (x) => {
    const [top, right, bottom, left] = x.dataset.coord
        .replace(/[ ()]/g, '')
        .split(',')
        .map(Number);
    return { top, right, bottom, left };
};

const markFaces = () => {
    const facesDom = document.querySelector('.crop-face');
    const pos = getCoords(facesDom);
    console.log(pos);
    hyperHTML.bind(facesDom)`<div class='face-square' style=${{
        top: pos.top,
        left: pos.left,
    }} ></div>`;
    return facesDom;
};
