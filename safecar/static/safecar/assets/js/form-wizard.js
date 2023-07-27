'use strict'; $(document).ready(function () {
    $("#basic-forms").steps({ headerTag: "h3", bodyTag: "fieldset", transitionEffect: "slideLeft", autoFocus: true });
    $("#verticle-wizard").steps({ headerTag: "h3", bodyTag: "fieldset", transitionEffect: "slide", stepsOrientation: "vertical", autoFocus: true 
    ,onFinished: function (event, currentIndex) {
        $("form").submit()
    }
    });
     $("#design-wizard").steps({ headerTag: "h3", bodyTag: "fieldset", transitionEffect: "slideLeft", autoFocus: true }); 
    var form = $("#example-advanced-form").show(); 
 
    /*.validate({ errorPlacement: function errorPlacement(error, element) { element.before(error); }, rules: { confirm: { equalTo: "#password-2" } } });*/
});

