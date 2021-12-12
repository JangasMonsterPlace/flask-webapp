const navItems = document.querySelectorAll('.category-nav-link');
const heading = document.querySelector('#job-id-heading');

// loop through navitems and add event listener

navItems.forEach((item) => {
  item.addEventListener('click', () => {
    // for (let i = 0; i < navItems.length; i++) {
    //   $(`#table_id-${i+1}`).DataTable().destroy();
    // }
    console.log('click');
    $.get(`/get_lda?job_id=${heading.getAttribute('data-job-id')}&category_id=${item.getAttribute('data-cat-id')}`, function (data, status) {
      console.log(data, status);
      if (status === 'success') {
        // load data into table
        $(`#table_id-${item.getAttribute('data-cat-id')}`).DataTable({
          data: data.lda,
          columns: [{ data: 'id' }, { data: 'job_id' }, { data: 'text' }, { data: 'timestamp' }, { data: 'topic_id' }],
        });
      }
    });
  });
});
