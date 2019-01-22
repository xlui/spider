package context

type Context struct {
	PageState    map[string]int
	ImageState   map[string]int
	PageChannel  chan *Page
	ParseChannel chan *Page
	ImageChannel chan *Image
}
