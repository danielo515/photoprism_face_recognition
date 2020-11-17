if (import.meta.hot) {
    import.meta.hot.accept(({ module }) => {
        import.meta.hot.invalidate();
    });
}

const toggleClass = (id, className) => {
    const classes = document.getElementById(id).classList;
    classes.toggle(className);
};

console.log('Danielo, eres puto, puto reputo');
