    function validateSubmitButton() {
      var inputsWithValues = 0;
      var selectsWithValues = 0;
      var myInputs = $("input.required");
      var mySelects = $("select.required");
      myInputs.each(function(e) {
        if ($(this).val() !== "") {
          inputsWithValues += 1;
        }
      });
      mySelects.each(function(e) {
        if ( $(this).val() !== null) {
          selectsWithValues += 1;
        }
      })

      if (inputsWithValues == myInputs.length && selectsWithValues == mySelects.length) {
        $("button[type=submit]").prop("disabled", false);
      } else {
        $("button[type=submit]").prop("disabled", true);
      }
    }
