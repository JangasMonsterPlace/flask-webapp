const navItems = document.querySelectorAll('.category-nav-link');
const heading = document.querySelector('#job-id-heading');

// loop through navitems and add event listener
navItems.forEach((item) => {
    item.addEventListener('click', () => {
    console.log('click');
    $.get(`/get_lda?job_id=${heading.getAttribute('data-job-id')}&category_id=${item.getAttribute('data-cat-id')}`, function (data, status) {
      console.log(data, status);
        if (status === 'success') {
        // load data into table
        $('#table_id').DataTable();
        }
    });
  });
});
