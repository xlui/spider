package context

import (
	"gospider/config"
	"io"
	"io/ioutil"
	"log"
	"net/http"
)

type Page struct {
	Url    string
	Body   *[]byte
	Parsed bool
}

type Image struct {
	Url    string
	File   string
	Folder string
}

type Context struct {
	PageState    map[string]int
	PageChannel  chan *Page
	ParseChannel chan *Page
	ImageChannel chan *Image
}

func (image *Image) Download(ctx *Context, client *http.Client) {

}

func (page *Page) Fetch(ctx *Context, client *http.Client) {
	if ctx.PageState[page.Url] == config.Success {
		return
	}

	request, err := http.NewRequest("GET", page.Url, nil)
	if err != nil {
		log.Fatalln("Failed to create new request!", err.Error())
	}

	response, err := client.Do(request)
	if err != nil {
		log.Fatalln("Failed  to request the url!", err.Error())
	}
	//noinspection GoUnhandledErrorResult
	defer response.Body.Close()

	reader := response.Body.(io.Reader)
	body, err := ioutil.ReadAll(reader)
	if err != nil {
		log.Fatalln("Failed to read from response body!", err.Error())
	}
	page.Body = &body
	ctx.PageState[page.Url] = config.Success
	ctx.ParseChannel <- page
}

func (page *Page) Parse(ctx *Context) {

}
