function flipPage() {
    const page1 = document.querySelector('.page1');
    const page2 = document.querySelector('.page2');

    if (page1.style.transform === 'rotateY(0deg)') {
        page1.style.transform = 'rotateY(180deg)';
        page2.style.transform = 'rotateY(0deg)';
    } else {
        page1.style.transform = 'rotateY(0deg)';
        page2.style.transform = 'rotateY(180deg)';
    }
}
