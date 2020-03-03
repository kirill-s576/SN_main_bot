var createCalculator = {

  getCalculation: function(num1,num2) {
    if(isNaN(num1) === true || typeof num1 === "string" || typeof num1 === undefined)
      {
       num1 = 0
       }
    if(isNaN(num2) === true || typeof num2 === "string" || typeof num2 === undefined)
      {
       num2 = 0
       }
  var calculation = num1+num2;
  return calculation
  }


}
createCalculator.getCalculation(10,20)