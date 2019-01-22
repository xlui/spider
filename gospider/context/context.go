package context

import (
	"gospider/image"
	"gospider/page"
)

type Context struct {
	PageState    map[string]int
	PageChannel  chan *page.Page
	ParseChannel chan *page.Page
	ImageChannel chan *image.Image
}
