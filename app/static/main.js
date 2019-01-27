$(document).ready(function() {
  let wrapper = $(".wrapper");
  let passInfo = $(".pass-info");
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

    if (password.length < 4) {
      msg = "Too short password";
    } else if (password.length > 32) {
      msg = "Too long password";
    } else if (!/^[a-zA-Z0-9@$!%*?&]+$/.test(password)) {
      msg = "Not allowed characters";
    } else {
      entropy = getEntropy(password);

      if (entropy < 28) {
        msg = "Very weak password";
      } else if (entropy < 36) {
        msg = "Weak password";
      } else if (entropy < 60) {
        msg = "Reasonable password";
      } else if (entropy < 128) {
        msg = "Strong password";
      } else {
        msg = "Very strong password";
      }
    }

    $(passInfo).text(msg);
  });

  function getEntropy(password) {
    if (/^[a-z]+$/.test(password) || /^[A-Z]+$/.test(password)) {
      return password.length * Math.log2(26);
    } else if (/^[0-9]+$/.test(password)) {
      return password.length * Math.log2(10);
    } else if (/^[@$!%*?&]+$/.test(password)) {
      return password.length * Math.log2(7);
    } else if (/^[a-zA-Z]+$/.test(password)) {
      return password.length * Math.log2(52);
    } else if (/^[a-z0-9]+$/.test(password) || /^[A-Z0-9]+$/.test(password)) {
      return password.length * Math.log2(36);
    } else if (/^[a-z@$!%*?&]+$/.test(password) || /^[A-Z@$!%*?&]+$/.test(password)) {
      return password.length * Math.log2(33);
    } else if (/^[a-zA-Z0-9]+$/.test(password)) {
      return password.length * Math.log2(62);
    } else if (/^[a-zA-Z@$!%*?&]+$/.test(password)) {
      return password.length * Math.log2(59);
    } else if (/^[a-z0-9@$!%*?&]+$/.test(password) || /^[A-Z0-9@$!%*?&]+$/.test(password)) {
      return password.length * Math.log2(43);
    } else {
      return password.length * Math.log2(69);
    }
  }
});