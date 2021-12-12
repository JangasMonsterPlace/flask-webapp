const navItems = document.querySelectorAll('.category-nav-link');
const heading = document.querySelector('#job-id-heading');

// loop through navitems and add event listener

let table;
console.log(table);
navItems.forEach((item) => {
  item.addEventListener('click', () => {
    try {
      table.destroy();
    } catch (error) {
      console.log(error);
    }
    console.log('click');
    $.get(`/get_lda?job_id=${heading.getAttribute('data-job-id')}&category_id=${item.getAttribute('data-cat-id')}`, function (data, status) {
      console.log(data, status);
      if (data.lda) {
        // load data into table
        table = $(`#table_id-${item.getAttribute('data-cat-id')}`).DataTable({
          data: data.lda,
          columns: [{ data: 'id' }, { data: 'job_id' }, { data: 'text' }, { data: 'timestamp' }, { data: 'topic_id' }],
        });
      } else {
        alert('No data found');
      }
    });
  });
});

// handle category naming
const submitCategoryRenaming = (input) => {
  console.log('click');
  const form = document.querySelector(`#rename-category-${input.value}`);
  console.log(form);
  const categoryName = form.querySelector('.cat-name').value;
  const description = form.querySelector('.cat-desc').value;
  const jobId = form.querySelector('.job-id').value;
  console.log({ job_id: jobId, category_id: input.value, name: categoryName, description: description });

  $.post('/name_lda', { job_id: jobId, category_id: input.value, name: categoryName, description: description }, function (data, status) {
    console.log(data, status);
    if (data.status === '201') {
      alert('Category name updated');
      location.reload();
    } else {
      alert('Error updating category name');
    }
  });
};
