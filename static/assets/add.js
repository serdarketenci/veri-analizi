// Copyright of Simternet Inc

$(document).ready(function() {
    window.setTimeout(function(){
   // function that checks the change in select features input box and hides the items that do not have the written string     
   $( "#select_features_input" ).change(function() {
       value = $('#select_features_input').val()
       a = $('.inputClassName_checklist');

       for(i=0; i < a.length; i++){
           // shows all of the items again in order to hide later
           a[i].nextSibling.parentNode.style.display = 'inline-block';
       }

       for(i=0; i < a.length; i++){
           // if the item does not have the written text, then it is hidden.
           if (a[i].nextSibling.textContent.toLowerCase().indexOf(value.toLowerCase()) < 0){
               a[i].nextSibling.parentNode.style.display = 'none';
           }}
   });
   }, 600);
});
