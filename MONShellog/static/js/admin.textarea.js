window.onload = function()
{
    // create the FCK Editor and replace the specific text area with it
    if (document.getElementById('id_body') != null)
    {
      var oFCKeditor = new FCKeditor('id_body') ;
      oFCKeditor.Width = '60%';
      oFCKeditor.Height = '500';
      oFCKeditor.BasePath = '/media/fckeditor/';
      oFCKeditor.ReplaceTextarea();
    }
}

