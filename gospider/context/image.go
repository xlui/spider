package context

import "net/http"

type Image struct {
	Url    string
	File   string
	Folder string
}

func (image *Image) Download(ctx *Context, client *http.Client) {

}
