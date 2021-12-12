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


$( "[name=ngram-detail]" ).click(function(){
  query_params = $(this).attr("data-ngram-sequence").split(",").join("&q=")

  $("#ngram-detail-info").text($(this).attr("data-ngram-sequence"))

  $.ajax({
    url: "/get-text-bodies-for-sequence?q=" + query_params,
    success: function(data){
      var time_series = [
        {
          x: data.time_aggregated_data.dates,
          y: data.time_aggregated_data.values,
          type: 'scatter'
        }
      ]
      Plotly.newPlot('ngram-detail-ts-plot', time_series);
      $('#ngram-detail-texts').empty()
      data.raw_text_data.forEach(function(element){
        var content = "<li class=\"list-group-item\">" + element.text + "</li>"
        $('#ngram-detail-texts').append(content)
      })
    }
  })
})