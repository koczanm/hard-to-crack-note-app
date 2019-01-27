$(document).ready(function() {
  let wrapper = $(".wrapper");
  let addButton = $(".is-adding");
  let deleteButton = $(".delete");
  let navbarBurger = $(".navbar-burger");
  let passwordInput = $("#password");

  $(addButton).click(function(e) {
    e.preventDefault();
    $(wrapper).append('<div class="field is-grouped"><div class="control"><input class="input" type="text" name="user"></div><div class="control"><button class="button is-danger is-removing">Remove</button></div></div>')
  });

  $(deleteButton).click(function(e) {
    $(this).parent().remove();
  });

  $(wrapper).on("click", ".is-removing", function(e) {
    e.preventDefault();
    $(this).parent().parent().remove();
  });

  $(navbarBurger).click(function() {
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });

  $(passwordInput).keyup(function() {
    let password = $(this).val();
    let entropy = 0;
    for (let i = 0; i < password.length; i++) {
    }
  });
});