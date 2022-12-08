const navSlide = () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.hide-data');
  console.log(burger);
  if(burger){
    burger.addEventListener('click', () => {
      console.log('i am in this shit');
      //toggle nav
      nav.classList.toggle('nav-active');
      console.log('toggle command is done');
      // burger animation
      burger.classList.toggle('toggle');
      // clearInterval(refreshID);
    });
}
}
// navSlide();
// let refreshID = setInterval(navSlide, 250);
setTimeout(navSlide, 5000);
navSlide();


var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
  document.body.appendChild(script);


var script = document.createElement('script');
  script.type = 'text/javascript';
  function googleTranslateElementInit() {
    new google.translate.TranslateElement(
      {pageLanguage: 'en'},
      'google_translate_element'
    );
  }
  document.body.appendChild(script);
