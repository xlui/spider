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

func (page *Page) Fetch(ctx *context.Context, client *http.Client) {

}

func (page *Page) Parse(ctx *context.Context) {

}
