$(document).ready(function(){
  // event handler for the query button in tables list
  $('.query-btn').click(function(){
    e.preventDefault(); // prevent reloading of page

      // save the  tables selected and button value for flask
    const selected_tables = [];
    $('.checkboxes :checked').each(function(){
      selected_tables.push($(this).val());
    });
    
    const btn_value = $this.val;
    
    $ajax({
      url:'/user/database/dynamic_tblheaders',
      type: 'POST',
      contentType: 'application/json',
      data: {"selected_tables": selected_tables,
             "options": btn_value},
      dataType: 'json',
      success: function(data){
        // fisrt part of html 
        let second_query = `
        <form action="${data.route}" method="POST">
        <dl>
          <dt>Please check one or more of the following</dt>
        `;
      //  loop through recieved headers list
          second_query += data.headers.map(item => {
            return `
              <dd><input class="checkboxes" type="checkbox" value="${item}" name="columns">
                <label>${item}</label>
              </dd>
            `;
          }).join('');

          // last part of html
          second_query += `
          </dl>
          <button class="query-btn" type="submit" name="action" value="Query">Query</button>
          <button type="submit" name="action" value="Delete">DELETE</button>
          </form>
      `;
          //  append complete html to template
       $('.query-container-2').append(second_query);
      }

    });

    // console.log(selected_tables);
    alert('Button clicked!');
    
  });
});