package context

import (
	"bytes"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"gospider/config"
	"gospider/utils"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"path"
)

type Page struct {
	Url    string
	Number int
	Body   *[]byte
	Parsed bool
}

func (page *Page) Fetch(ctx *Context, client *http.Client) {
	log.Println("Fetch: fetching images from page", page.Url)

	request, err := http.NewRequest("GET", page.Url, nil)
	utils.CheckError(err, "Failed to create new request!")

	response, err := client.Do(request)
	utils.CheckError(err, "Failed to request the url!")
	//noinspection GoUnhandledErrorResult
	defer response.Body.Close()

	reader := response.Body.(io.Reader)
	body, err := ioutil.ReadAll(reader)
	utils.CheckError(err, "Failed to read from response body!")

	page.Body = &body
	ctx.PageLock.Lock()
	ctx.PageState[page.Url] = config.Success
	ctx.PageLock.Unlock()
	ctx.ParseChannel <- page
}

func (page *Page) Parse(ctx *Context) {
	log.Println("Parse: parsing html tags in page", page.Url)
	doc, err := goquery.NewDocumentFromReader(bytes.NewReader(*(page.Body)))
	utils.CheckError(err, "Failed to create query document for page body")

	count := 1
	// find element through css selector
	doc.Find(config.PicSelector).Each(func(i int, selection *goquery.Selection) {
		href, exist := selection.Attr("href")
		if !exist || href == "" {
			return
		}
		if selection.Text() == config.PicMark {
			// mark image as ready for download
			ctx.ImageLock.Lock()
			ctx.ImageState[href] = config.Ready
			ctx.ImageLock.Unlock()
			folder := fmt.Sprint(config.Storage, page.Number, "/")
			filename := fmt.Sprint(folder, count, path.Ext(href))
			count++
			ctx.ImageChannel <- &Image{Url: href, File: filename, Folder: folder}
		}
	})
}
