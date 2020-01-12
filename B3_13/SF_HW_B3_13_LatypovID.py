class HTML:
    def __init__(self, output = None, klass=None, level = 0, **kwargs):
        self.output = output
        self.attributes = {}
        self.children = []
        self.tag = "html"
        self.level = level
        self.result = ""

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value
       
    def __enter__(self):
        return self

    def __add__(self, other):
        self.children.append(other)
        other.level = self.level
        return self
    
    def __exit__(self, type, value, traceback):
        print(str(self))
        if self.output is not None: 
            with open(self.output, "w") as fp:
                fp.write(self.result)
    
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('{attribute}="{value}"'.format(attribute=attribute, value=value))
        attrs = " ".join(attrs)        

        self.result =(" "*4*self.level+"<{tag} {attrs}>" + "\n").format(tag=self.tag, attrs=attrs)
        for child in self.children:
            self.result += str(child)
        self.result += (" "*4*self.level+"</{tag}>"+"\n").format(tag=self.tag)
        return self.result
        
class TopLevelTag:
    def __init__(self, tag, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children = []
        self.level = 0

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value
                
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
            
    def __add__(self, other):
        self.children.append(other)
        other.level = self.level + 1
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('{attribute}="{value}"'.format(attribute=attribute, value=value))
        attrs = " ".join(attrs)

        if self.children:
            opening = " "*4*self.level + "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "{text}".format(text=self.text)
            for child in self.children:
                internal += str(child)
            ending = " "*4*self.level + "</{tag}>".format(tag=self.tag)
            return opening+'\n'+ internal + ending + "\n" 
        else:
            return (" "*4*self.level + "<{tag} {attrs}>\n"+" "*4*(self.level+1)+"{text}\n"+" "*4*self.level+"</{tag}>" + "\n").format(tag=self.tag, attrs=attrs, text=self.text)    
    
class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.level = 0

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value
                
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
            
    def __add__(self, other):
        self.children.append(other)
        other.level = self.level + 1
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('{attribute}="{value}"'.format(attribute=attribute, value=value))
        attrs = " ".join(attrs)
        
        if self.children:
            opening = " "*4*self.level + "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "{text}".format(text=self.text)
            for child in self.children:
                internal += str(child)
            ending = " "*4*self.level+"</{tag}>".format(tag=self.tag)
            return opening  + "\n" + internal + ending + "\n" 
        else:
            if self.is_single:
                return (" "*4*self.level + "<{tag} {attrs}/>" + "\n").format(tag=self.tag, attrs=attrs)
            else:
                return (" "*4*self.level + "<{tag} {attrs}>\n"+" "*4*(self.level+1)+"{text}\n"+" "*4*self.level+"</{tag}>" + "\n").format(tag=self.tag, attrs=attrs, text=self.text)

def main(output=None):
    with HTML(output=output, lang="en") as doc:
        with TopLevelTag("head") as head:
            doc += head
            with Tag("title") as title:
                head += title
                title.text = "hello"

        with TopLevelTag("body") as body:
            doc += body
            with Tag("h1", klass=("main-text",)) as h1:
                body += h1
                h1.text = "Test"

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                body += div
                with Tag("p") as paragraph:
                    div += paragraph
                    paragraph.text = "another test"

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

if __name__ == "__main__":
    main("b3-hw.html")