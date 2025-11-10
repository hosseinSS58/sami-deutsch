document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('[data-newsletter-form]');

  forms.forEach((form) => {
    const emailInput = form.querySelector('input[type="email"]');
    const submitButton = form.querySelector('button[type="submit"]');
    const feedback = form.parentElement.querySelector('.newsletter-feedback');
    const originalButtonContent = submitButton ? submitButton.innerHTML : null;

    const renderMessage = (message, level) => {
      if (!feedback) {
        return;
      }
      feedback.innerHTML = [
        `<div class="alert alert-${level} alert-dismissible fade show" role="alert">`,
        message,
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>',
      ].join('');
    };

    const resetButton = () => {
      if (submitButton && originalButtonContent !== null) {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
      }
    };

    form.addEventListener('submit', (event) => {
      event.preventDefault();

      if (!emailInput) {
        return;
      }

      const emailValue = emailInput.value.trim();

      if (!emailValue) {
        emailInput.classList.add('is-invalid');
        renderMessage('لطفاً ایمیل خود را وارد کنید.', 'danger');
        return;
      }

      if (!emailInput.checkValidity()) {
        emailInput.classList.add('is-invalid');
        renderMessage('لطفاً یک ایمیل معتبر وارد کنید.', 'danger');
        return;
      }

      emailInput.classList.remove('is-invalid');

      if (submitButton && originalButtonContent !== null) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>ثبت نام...';
      }

      // Simulate asynchronous submission
      window.setTimeout(() => {
        renderMessage('عضویت شما با موفقیت ثبت شد! 🎉', 'success');
        form.reset();
        resetButton();
      }, 800);
    });

    emailInput?.addEventListener('input', () => {
      emailInput.classList.remove('is-invalid');
    });
  });
});

