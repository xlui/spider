package page

import (
	"gospider/context"
	"net/http"
)

type Page struct {
	Url    string
	Body   []byte
	Parsed bool
}

func (page *Page) fetch(ctx *context.Context, client *http.Client) {

}