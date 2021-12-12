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
const categorySubmitBtn = document.querySelectorAll('.name-category-button');

categorySubmitBtn.forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const categoryId = btn.getAttribute('data-category-id');
    const categoryName = document.querySelector(`#category-name-${categoryId}`).value;
    console.log(categoryName);
    $.post('/name_lda', { category_id: categoryId, name: categoryName, description: description }, function (data, status) {
      console.log(data, status);
      if (data.success) {
        alert('Category name updated');
        location.reload();
      } else {
        alert('Error updating category name');
      }
    });
  });
});
