
function addToCart(id,name,price){
    event.preventDefault() /*ban chat cua the <a> chuyen trang khi click thi reload, de ngan chan reload de thuc thi dung 1 function thi dung event.preventDefault*/
    /*fetch cua window tich hop san de gui request len server javascript*/
    fetch('/api/add-cart',{
        method:'post',
        body: JSON.stringify({
            'id':id,
            'name':name,
            'price':price
        }),
        headers:{
            'Content-Type':'application/json'
        }

    }).then(function(response){
        console.info(response)
        return response.json()
    }).then(function (data){
        console.info(data)
        /*let counter = document.getElementById('cartCounter')*/
        let counter = document.getElementsByClassName('cart-counter')
        for( let i = 0 ; i < counter.length; i++){
            counter[i].innerText = data.total_quantity
        }

    }).catch(function (err){
        console.error(err)
    })
}



function paymentHandle(){
    if(confirm('Are you sure to payment ?') == true){
            fetch('/api/payment',{
            method:'post'
        }).then(response => response.json()).then(data => {
            if (data.code == 200){
                location.reload()
            }
        }).catch(err =>{
            console.error(err)
        })
    }
}



function updateCart(id, obj){
    fetch('/api/update-cart',{
        method: 'put',
        body:JSON.stringify({
            'id':id,
            'quantity':parseInt(obj.value)
        }),
        headers:{
        'Content-Type':'application/json'
        }
    }).then(response => response.json()).then(data => {
        console.info(data)
        let counter = document.getElementsByClassName('cart-counter')
        for( let i = 0 ; i < counter.length; i++){
            counter[i].innerText = data.total_quantity
        }
        let amount = document.getElementById('total-amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}