package context

import (
	"gospider/image"
	"gospider/page"
)

type Context struct {
	PageState map[string]string

	PageChannel chan *page.Page
	ImageChannel chan *image.Image
}
