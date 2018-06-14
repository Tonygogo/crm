function searchCustomerContribute() {
    $("#dg").datagrid('load', {
        customerName: $("#s_customerName").val()
    })
}