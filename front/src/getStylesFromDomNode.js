/**
 *
 * @param {string} id the dom-node to extract styles from
 * @returns {Object} an object with the applied styles
 */
export function getStylesFromDomNode(id) {
    const node = document.getElementById(id);
    if (!node) return {};
    const domStyles = node.style;
    // By converting the CSSStyleDeclaration to an array we get only the relevant properties
    const style = Array.from(domStyles).reduce((res, key) => {
        res[key] = domStyles[key];
        return res;
    }, {});
    return style;
}
