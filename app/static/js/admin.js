//JS For edit product to get its info
function get_product_info(url, id) {
    $.getJSON(url, function(data) {
        $('#editName').val(data.pro_name);
        $('#editPerson').val(data.person);
        $('#product_id').val(id);
        $('#editProductModel').modal();
    });
}

//Js For submit product id to delete product
function delPro(productid) {
    $('#proClick').click(function () {
        formSubmit(productid);
    });
    $('#delProModel').modal();
}
function formSubmit(productid) {
    $('#delForm' + productid).submit();
}

//JS For submit package id to delete article
function delPack(packageid) {
    $('#packClick').click(function () {
        formSubmit(packageid);
    });
    $('#delPackModel').modal();
}
function formSubmit(packageid) {
    $('#delForm' + packageid).submit();
}