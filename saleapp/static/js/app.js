function addComment(productId){
    let content = document.getElementById('commentInfo')
    if( content !== null){
        fetch('/api/comments',{
            method: 'post',
            body:JSON.stringify({
                'product_id':productId,
                'content':content.value
            }),
            headers:{
            'Content-Type':'application/json'
            }
        }).then(response => response.json()).then(data =>{
            console.info(data)
           /* if(data.status == 201){
                let comments = document.getElementById('commentArea')
                comments.innerHTML = getHtmlComment(data) + comments.innerHTML
            }
            else{
                alert("Add failed !")
            }*/
            if(data.status == 201){
                let c = data.comment
                let area = document.getElementById('commentArea')
                /*area.innerHTML =`
                    <div class="display-content-comment" style="margin-left:10rem;">
                        <div class="show-avatar" style="max-width:100%;">
                            <img style="width:70px;height:70px;border-radius:50%;" src="${ c.user.avatar }" alt="demo"/>
                        </div>
                        <p><span>${ c.user.username }</span></p>
                        <br><br>
                        <div>
                            <p>${c.content}</p>
                            <p><em>${c.created_date}</em></p>
                        </div>
                    </div>
                `+ area.innerHTML*/
                    area.innerHTML = getHtmlComment(c) + area.innerHTML
            }else if(data.status == 404){
                alert(data.err_msg)
            }
        }).catch(err => console.error(err))

    }

}




function loadComments(product_id,page=1){
    fetch(`/api/products/${product_id}/comments?page=${page}`).then(response => response.json()).then(data => {
        console.info(data)
        let comments = document.getElementById('commentArea')
        comments.innerHTML = ""
        for(let i = 0; i < data.length; i ++){

            comments.innerHTML += getHtmlComment(data[i])
        }
    })
}

function getHtmlComment(comment){

    const image = comment.user.avatar
    const name = comment.user.username
    if(image === null || !image.startsWith('https')){
        image = 'static/image/behacute.jpg'
    }

    return `
           <div class="display-content-comment" style="margin-left:10rem; ">
                <div class="show-avatar" style="max-width:100%;">
                    <img style="width:70px;height:70px;border-radius:50%;" src="${image}" alt="${name}"/>
                </div>
                <p><span>${name}</span></p>
                <br><br>
                <div >
                    <p>${comment.content}</p>
                    <p style="color:gray;"><em>${moment(comment.created_date).locale('vi').fromNow()}</em></p>
                </div>
           </div>
    `
}
